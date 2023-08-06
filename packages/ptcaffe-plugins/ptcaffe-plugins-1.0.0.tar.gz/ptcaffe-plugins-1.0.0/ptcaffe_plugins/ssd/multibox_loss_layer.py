# -*- coding:utf-8 -*- 
from __future__ import division, print_function

import torch
import torch.nn as nn
import torch.nn.functional as F

import numpy as np
from collections import OrderedDict
from ptcaffe.layer_dict import register_loss_layer

from .bbox_utils import *

@register_loss_layer('MultiBoxLoss')
class MultiBoxLoss(nn.Module):
    """SSD Weighted Loss Function
    Compute Targets:
        1) Produce Confidence Target Indices by matching  ground truth boxes
           with (default) 'priorboxes' that have jaccard index > threshold parameter
           (default threshold: 0.5).
        2) Produce localization target by 'encoding' variance into offsets of ground
           truth boxes and their matched  'priorboxes'.
        3) Hard negative mining to filter the excessive number of negative examples
           that comes with using a large number of default bounding boxes.
           (default negative:positive ratio 3:1)
    Objective Loss:
        L(x,c,l,g) = (Lconf(x, c) + ¦Áloc(x,l,g)) / N
        Where, Lconf is the CrossEntropy Loss and Lloc is the SmoothL1 Loss
        weighted by ¦Áwhich is set to 1 by cross val.
        Args:
            c: class confidences,
            l: predicted boxes,
            g: ground truth boxes
            N: number of matched default boxes
        See: https://arxiv.org/pdf/1512.02325.pdf for more details.
    """

    #def __init__(self, num_classes, overlap_thresh, prior_for_matching,
    #             bkg_label, neg_mining, neg_pos, neg_overlap, focal_loss=True, alpha=0.5):
    def __init__(self, layer, *input_shapes):
        super(MultiBoxLoss, self).__init__()
        self.loss_weight = float(layer.get('loss_weight', 1.0))
        num_classes = int(layer['multibox_loss_param']['num_classes'])
        overlap_thresh = float(layer['multibox_loss_param']['overlap_threshold'])
        prior_for_matching = layer['multibox_loss_param']['use_prior_for_matching'] == 'true'
        bkg_label = int(layer['multibox_loss_param']['background_label_id'])
        neg_mining = True
        neg_pos = float(layer['multibox_loss_param']['neg_pos_ratio'])
        neg_overlap = float(layer['multibox_loss_param']['neg_overlap'])
        alpha = 0.25

        self.num_classes = num_classes
        self.threshold = overlap_thresh
        self.background_label = bkg_label
        assert(self.background_label == 0)
        self.use_prior_for_matching = prior_for_matching
        self.do_neg_mining = neg_mining
        self.negpos_ratio = neg_pos
        self.neg_overlap = neg_overlap
        self.variance = [0.1, 0.2]
        self.scale_compensation = False
        self.rpn_match = False
        if 'scale_compensation' in layer['multibox_loss_param'] and layer['multibox_loss_param']['scale_compensation'] == 'true':
            self.scale_compensation = True
        print('scale_compensation in multiboxloss is', self.scale_compensation)
        if 'rpn_match' in layer['multibox_loss_param'] and layer['multibox_loss_param']['rpn_match'] == 'true':
            self.rpn_match = True
        print('rpn_match in multiboxloss is', self.rpn_match)
        self.work_on_cpu = True
        if 'work_on_cpu' in layer['multibox_loss_param'] and layer['multibox_loss_param']['work_on_cpu'] == 'false':
            self.work_on_cpu = False
        print('work_on_cpu in multiboxloss is', self.work_on_cpu)
        self.normalization  = layer['loss_param']['normalization']
        print('normalization = %s' % self.normalization)

    def forward_shape(self, loc_shape, conf_shape, prior_shape, target_shape):
        return [1,]

    def forward(self, loc_data, conf_data, priors, targets):
        """Multibox Loss
        Args:
            predictions (tuple): A tuple containing loc preds, conf preds,
            and prior boxes from SSD net.
                conf shape: torch.size(batch_size,num_priors,num_classes)
                loc shape: torch.size(batch_size,num_priors,4)
                priors shape: torch.size(num_priors,4)
            ground_truth (tensor): Ground truth boxes and labels for a batch,
                shape: [batch_size,num_objs,5] (last idx is the label).
        """
        # if gpu memory is not enough
        if loc_data.data.is_cuda:
            device_id = loc_data.data.get_device()

        if self.work_on_cpu:
            loc_data = loc_data.cpu()
            conf_data = conf_data.cpu()
            priors = priors.cpu()
            targets = targets.cpu()

        if loc_data.data.is_cuda:
            use_gpu = True
        else:
            use_gpu = False

        num = loc_data.size(0)
        num_priors = (loc_data.size(1)//4)
        num_classes = self.num_classes
        loc_data = loc_data.view(num, num_priors, 4)
        conf_data = conf_data.view(num, num_priors, num_classes)
        priors = priors[0][0].view(num_priors, 4)
        targets = targets.view(-1, 8)

        # match priors (default boxes) and ground truth boxes
        loc_t = torch.Tensor(num, num_priors, 4)
        conf_t = torch.zeros(num, num_priors).long()
        for idx in range(num):
            sub_mask = (targets[:,0] == idx)
            if sub_mask.data.float().sum() == 0:
                continue
            sub_targets = targets[sub_mask.view(-1,1).expand_as(targets)].view(-1,8)
            truths = sub_targets[:, 3:7].data
            labels = sub_targets[:, 1].data
            defaults = priors.data
            defaults = center_size(defaults)
            if self.scale_compensation:
                match_sc(self.threshold, truths, defaults, self.variance, labels,
                      loc_t, conf_t, idx)
            elif self.rpn_match:
                match_rpn(self.threshold, truths, defaults, self.variance, labels,
                      loc_t, conf_t, idx)
            else:
                match(self.threshold, truths, defaults, self.variance, labels,
                      loc_t, conf_t, idx)

        if use_gpu:
            loc_t = loc_t.cuda(device_id)
            conf_t = conf_t.cuda(device_id)

        pos = conf_t > 0
        num_pos = pos.sum(1, keepdim=True)

        # Localization Loss (Smooth L1)
        # Shape: [batch,num_priors,4]
        pos_idx = pos.unsqueeze(pos.dim()).expand_as(loc_data)
        loc_p = loc_data[pos_idx].view(-1, 4)
        loc_t = loc_t[pos_idx].view(-1, 4)
        loss_l = F.smooth_l1_loss(loc_p, loc_t, size_average=False)

        # Compute max conf across batch for hard negative mining
        batch_conf = conf_data.view(-1, self.num_classes)

        if True:
            loss_c = log_sum_exp(batch_conf).view(-1,1) - batch_conf.gather(1, conf_t.view(-1, 1))

            # Hard Negative Mining
            loss_c[pos.view(-1, 1)] = 0  # filter out pos boxes for now
            loss_c = loss_c.view(num, -1)
            _, loss_idx = loss_c.sort(1, descending=True)
            _, idx_rank = loss_idx.sort(1)
            num_pos = pos.long().sum(1, keepdim=True)

            num_neg = torch.clamp(self.negpos_ratio*num_pos.data.float(), max=pos.size(1)-1).long()
            N = num_pos.data.sum()
            if N > 0:
                neg = idx_rank < num_neg.expand_as(idx_rank)
                # Confidence Loss Including Positive and Negative Examples
                pos_idx = pos.unsqueeze(2).expand_as(conf_data)
                neg_idx = neg.unsqueeze(2).expand_as(conf_data)
                conf_p = conf_data[(pos_idx+neg_idx).gt(0)].view(-1, self.num_classes)
                targets_weighted = conf_t[(pos+neg).gt(0)]
                loss_c = F.cross_entropy(conf_p, targets_weighted, size_average=False)

                # Sum of losses: L(x,c,l,g) = (Lconf(x, c) + ¦Áloc(x,l,g)) / N

                loss_l /= float(N)
                loss_c /= float(N)
            else:
                loss_l = torch.zeros(1, requires_grad = True)
                loss_c = torch.zeros(1, requires_grad = True)
            if (not use_gpu) or loss_l.data.get_device() == 0:
                if False:
                    print('loss_l = %f, loss_c = %f' % (loss_l.data[0], loss_c.data[0]))
                if debug_flag:
                    print('pytorch num_pos = %s, num_neg = %s' % (list(num_pos.data.view(-1)), list(num_neg.data.view(-1))))
                    print('[%d] pytorch loss_l = %f, loss_c = %f, loss = %f, N = %d' % (device_id, loss_l.data[0], loss_c.data[0], loss_l.data[0]+loss_c.data[0], N))
            loss = loss_l.view(-1) + loss_c.view(-1)
            if self.work_on_cpu:
                return loss.cuda()
            else:
                return loss
