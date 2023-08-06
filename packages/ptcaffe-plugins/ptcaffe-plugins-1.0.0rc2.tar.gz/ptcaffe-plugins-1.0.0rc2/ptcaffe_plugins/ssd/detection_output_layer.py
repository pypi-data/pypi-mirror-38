from __future__ import division, print_function

import threading

import torch
import torch.nn as nn

import numpy as np
from collections import OrderedDict
from ptcaffe.layer_dict import register_layer

from .bbox_utils import *

@register_layer('DetectionOutput')
class DetectionOutput(nn.Module):
    VOC_CLASSES = ('__background__', 'aeroplane', 'bicycle', 'bird', 'boat', 'bottle', 'bus', 'car', 'cat', 'chair', 'cow', 'diningtable', 'dog', 'horse', 'motorbike', 'person', 'pottedplant', 'sheep', 'sofa', 'train', 'tvmonitor')
    PEDFACE_CLASSES = ('__background__', 'pedestrian', 'face')

    """At test time, Detect is the final layer of SSD.  Decode location preds,
    apply non-maximum suppression to location predictions based on conf
    scores and threshold to a top_k number of output predictions for both
    confidence score and locations.
    """
    #def __init__(self, num_classes, bkg_label, top_k, conf_thresh, nms_thresh, keep_top_k):
    def __init__(self, layer, *input_shapes):
        super(DetectionOutput, self).__init__()
        detection_output_param = layer.get('detection_output_param', OrderedDict())
        self.num_classes = int(detection_output_param['num_classes'])
        bkg_label = int(layer['detection_output_param']['background_label_id'])
        top_k = int(layer['detection_output_param']['nms_param']['top_k'])
        keep_top_k = int(layer['detection_output_param']['keep_top_k'])
        conf_thresh = float(layer['detection_output_param']['confidence_threshold'])
        nms_thresh = float(layer['detection_output_param']['nms_param']['nms_threshold'])
        nms_param = layer['detection_output_param']['nms_param']
        self.nms_type = nms_param.get('nms_type', 'nms')

        self.background_label = bkg_label
        self.top_k = top_k
        # Parameters used in nms.
        self.nms_thresh = nms_thresh
        if nms_thresh <= 0:
            raise ValueError('nms_threshold must be non negative.')
        self.conf_thresh = conf_thresh
        self.keep_top_k = keep_top_k
        self.variance = [0.1, 0.2]

    def forward_shape(self, *layer_shapes):
        return [1,1,1,7]

    def forward(self, loc, conf, prior):
        """
        Args:
            loc: (tensor) Loc preds from loc layers
                Shape: [batch,num_priors*4]
            conf: (tensor) Shape: Conf preds from conf layers
                Shape: [batch, num_priors*num_classes]
            prior: (tensor) Prior boxes and variances from priorbox layers
                Shape: [1,2, num_priors*4]
        """
        dets_dict = dict()

        num = loc.size(0)
        loc_data = loc.data
        conf_data = conf.data
        prior_data = prior.data

        num_classes = self.num_classes
        num_priors = prior_data.size(2)/4

        conf_data  = conf_data.view(num, num_priors, self.num_classes).transpose(2, 1)
        prior_data = center_size(prior_data[0][0].view(-1,4))

        outputs = []
        for i in range(num):
            # Decode predictions into bboxes.
            loc_data_i = loc_data[i].view(-1, 4)
            decoded_boxes = decode(loc_data[i].view(-1, 4), prior_data, self.variance)
            #decoded_boxes = clip_boxes(decoded_boxes)
            #print("===ptcaffe=== %d len(decode_bboxes) = %d" % (i, len(decoded_boxes)))
    
            # For each class, perform nms
            num_det = 0
            #cls = 1
            image_outputs = []
            for cls in range(1, num_classes):
                c_mask = conf_data[i][cls].gt(self.conf_thresh)
                if c_mask.sum() == 0:
                    continue
                #print('===ptcaffe c_mask.sum() = %d' % c_mask.sum())
                scores = conf_data[i][cls][c_mask]
                l_mask = c_mask.unsqueeze(1).expand_as(decoded_boxes)
                boxes = decoded_boxes[l_mask].view(-1, 4)
                # idx of highest scoring and non-overlapping boxes per class
                if self.nms_type == "soft_nms":
                    from ptcaffe.utils.utils import add_local_path
                    add_local_path('lib')
                    from nms.cpu_nms import cpu_soft_nms
                    dets = torch.cat((boxes, scores.unsqueeze(1)), 1)
                    result = torch.FloatTensor(soft_nms(cpu_soft_nms, dets.cpu().numpy()))
                    result = torch.cat((result[:,4].unsqueeze(1), result[:,:4]), 1)
                    count = result.shape[0]
                    count = min(count, self.keep_top_k)
                else:
                    ids, count = nms(boxes, scores, self.nms_thresh, self.top_k)
                    #print("===ptcaffe=== %d:%d %d bboxes left after nms" % (i, cls, count))
                    count = min(count, self.keep_top_k)
                    result = torch.cat((scores[ids[:count]].unsqueeze(1), boxes[ids[:count]]), 1).to(conf.device)
                extra_info = torch.FloatTensor([i, cls]).view(1,2).expand(count,2).to(conf.device)
                #extra_info = conf.data.new().resize_(extra_info.size()).copy_(extra_info)
                output = torch.cat((extra_info[:count], result), 1)
                image_outputs.append(output.view(1,1,-1,7))
            image_outputs = torch.cat(image_outputs, dim=2)

            # keep_top_k
            if image_outputs.shape[2] > self.keep_top_k:
                image_outputs = image_outputs.view(-1, 7)
                image_outputs = image_outputs[image_outputs[:,2].sort(descending=True)[1]][:self.keep_top_k,:]
                if False: #self.debug_with_caffe:
                    image_outputs = image_outputs[image_outputs[:,1].sort()[1]]
                    image_outputs = image_outputs[image_outputs[:,0].sort()[1]]
                image_outputs = image_outputs.view(1, 1, -1, 7)

            outputs.append(image_outputs)
        outputs = torch.cat(outputs, dim=2)

        return outputs


