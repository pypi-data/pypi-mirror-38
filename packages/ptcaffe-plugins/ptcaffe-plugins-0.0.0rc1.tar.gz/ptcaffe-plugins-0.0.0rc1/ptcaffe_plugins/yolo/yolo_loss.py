from __future__ import division
import time
import torch
import math
import torch.nn as nn
import torch.nn.functional as F
from .utils import *
from ptcaffe.utils.logger import logger
from ptcaffe.utils.config import cfg
from collections import OrderedDict
import copy

# num_anchors: the total number or anchors
# nA: the masked number of anchors 
# nAnchors: nA*nH*nW
def build_targets(pred_boxes, target, anchors, masked_anchors, anchor_mask, num_anchors, num_classes, nH, nW, sil_thresh, seen):
    nB = target.size(0)
    nA = len(anchor_mask)
    nC = num_classes
    anchor_step = int(len(anchors)/num_anchors)
    assert(anchor_step == 2)
    coord_scale = torch.ones(nB, nA, nH, nW)
    tx         = torch.zeros(nB, nA, nH, nW) 
    ty         = torch.zeros(nB, nA, nH, nW) 
    tw         = torch.zeros(nB, nA, nH, nW) 
    th         = torch.zeros(nB, nA, nH, nW) 
    tconf      = torch.zeros(nB, nA, nH, nW)
    tcls       = torch.ones(nB, nA, nC, nH, nW) * -1

    nAnchors = nA*nH*nW
    nPixels  = nH*nW
    for b in range(nB):
        cur_pred_boxes = pred_boxes[b*nAnchors:(b+1)*nAnchors].t()
        cur_ious = torch.zeros(nAnchors)
        for t in range(target.shape[1]//5):
            if target[b][t*5+1] == 0:
                break
            gx = target[b][t*5+1]*nW
            gy = target[b][t*5+2]*nH
            gw = target[b][t*5+3]*nW
            gh = target[b][t*5+4]*nH
            cur_gt_boxes = torch.FloatTensor([gx,gy,gw,gh]).repeat(nAnchors,1).t()
            cur_ious = torch.max(cur_ious, bbox_ious(cur_pred_boxes, cur_gt_boxes, x1y1x2y2=False))
        tconf[b][(cur_ious>sil_thresh).view(nA, nH, nW)] = -1
        #print('silent index:', (cur_ious>sil_thresh).nonzero())
    if False: #seen < 12800:
       if anchor_step == 4:
           tx = torch.FloatTensor(masked_anchors).view(nA, anchor_step).index_select(1, torch.LongTensor([2])).view(1,nA,1,1).repeat(nB,1,nH,nW)
           ty = torch.FloatTensor(masked_anchors).view(nA, anchor_step).index_select(1, torch.LongTensor([2])).view(1,nA,1,1).repeat(nB,1,nH,nW)
       else:
           tx.fill_(0.5)
           ty.fill_(0.5)
       tw.zero_()
       th.zero_()
       coord_scale.fill_(1)

    nGT = 0
    nCorrect = 0
    for b in range(nB):
        for t in range(target.shape[1]//5):
            if target[b][t*5+1] == 0:
                break
            nGT = nGT + 1
            best_iou = 0.0
            best_n = -1
            min_dist = 10000
            gx = target[b][t*5+1].item() * nW
            gy = target[b][t*5+2].item() * nH
            gw = target[b][t*5+3].item() * nW
            gh = target[b][t*5+4].item() * nH

            gi = int(gx)
            gj = int(gy)
            gt_box = [0, 0, gw, gh]
            for n in range(num_anchors):
                aw = anchors[anchor_step*n]
                ah = anchors[anchor_step*n+1]
                anchor_box = [0, 0, aw, ah]
                iou  = bbox_iou(anchor_box, gt_box, x1y1x2y2=False)
                if anchor_step == 4:
                    ax = anchors[anchor_step*n+2]
                    ay = anchors[anchor_step*n+3]
                    dist = pow(((gi+ax) - gx), 2) + pow(((gj+ay) - gy), 2)
                if iou > best_iou:
                    best_iou = iou
                    best_n = n
                elif anchor_step==4 and iou == best_iou and dist < min_dist:
                    best_iou = iou
                    best_n = n
                    min_dist = dist

            if best_n in anchor_mask:
                best_id = anchor_mask.index(best_n)
              
                gt_box = [gx, gy, gw, gh]
                pred_box = pred_boxes[b*nAnchors+best_id*nPixels+gj*nW+gi]
    
                coord_scale[b][best_id][gj][gi] = 2.0 - gw*gh/nPixels
                tx[b,best_id,gj,gi] = target[b][t*5+1] * nW - gi
                ty[b,best_id,gj,gi] = target[b][t*5+2] * nH - gj
                tw[b,best_id,gj,gi] = math.log(gw/masked_anchors[anchor_step*best_id])
                th[b,best_id,gj,gi] = math.log(gh/masked_anchors[anchor_step*best_id+1])
                iou = bbox_iou(gt_box, pred_box, x1y1x2y2=False) # best_iou
                if tconf[b,best_id,gj,gi] == -1:
                    tcls[b,best_id,:,gj,gi] = 0
                tconf[b,best_id,gj,gi] = 1
                cls_id = int(target[b][t*5])
                tcls[b,best_id,cls_id,gj,gi] = 1
                if iou > 0.5:
                    nCorrect = nCorrect + 1

    return nGT, nCorrect, coord_scale, tx, ty, tw, th, tconf, tcls

class YoloLoss(nn.Module):
    def __init__(self, stride, anchor_mask=[], num_classes=0, anchors=[], num_anchors=1, ignore_thresh=0.6, truth_thresh=1.0,conf_thresh=0.7):
        super(YoloLoss, self).__init__()
        self.stride = stride
        self.anchor_mask = anchor_mask
        self.num_classes = num_classes
        self.anchors = anchors
        self.num_anchors = num_anchors
        self.anchor_step = int(len(anchors)/num_anchors)
        assert(self.anchor_step == 2)
        self.thresh = conf_thresh 
        self.ignore_thresh = ignore_thresh
        self.truth_thresh = truth_thresh
        self.seen = [0]
            
        self.anchors = [anchor/self.stride for anchor in self.anchors]
        masked_anchors = []
        for m in self.anchor_mask:
            start_ind = int(m*self.anchor_step)
            end_ind = int((m+1)*self.anchor_step)
            masked_anchors += self.anchors[start_ind:end_ind]
        self.masked_anchors = masked_anchors

    def forward(self, input, target=None):
        if self.training:
            #input : BxAs*(4+1+num_classes)*H*W
            t0 = time.time()
            nB = input.data.size(0)
            nA = len(self.anchor_mask)
            nC = self.num_classes
            nH = input.data.size(2)
            nW = input.data.size(3)
            device = input.data.device #get_device()
    
            output   = input.view(nB, nA, (5+nC), nH, nW)
            x    = F.sigmoid(output.index_select(2, torch.LongTensor([0]).to(device)).view(nB, nA, nH, nW))
            y    = F.sigmoid(output.index_select(2, torch.LongTensor([1]).to(device)).view(nB, nA, nH, nW))
            w    = output.index_select(2, torch.LongTensor([2]).to(device)).view(nB, nA, nH, nW)
            h    = output.index_select(2, torch.LongTensor([3]).to(device)).view(nB, nA, nH, nW)
            conf = F.sigmoid(output.index_select(2, torch.LongTensor([4]).to(device)).view(nB, nA, nH, nW))
            cls  = F.sigmoid(output.index_select(2, torch.linspace(5,5+nC-1,nC).long().to(device)).view(nB,nA,nC,nH,nW))
            t1 = time.time()
    
            pred_boxes = torch.FloatTensor(4, nB*nA*nH*nW).to(device)
            grid_x = torch.linspace(0, nW-1, nW).repeat(nH,1).repeat(nB*nA, 1, 1).view(nB*nA*nH*nW).to(device)
            grid_y = torch.linspace(0, nH-1, nH).repeat(nW,1).t().repeat(nB*nA, 1, 1).view(nB*nA*nH*nW).to(device)
            anchor_w = torch.Tensor(self.masked_anchors).view(nA, self.anchor_step).index_select(1, torch.LongTensor([0])).to(device)
            anchor_h = torch.Tensor(self.masked_anchors).view(nA, self.anchor_step).index_select(1, torch.LongTensor([1])).to(device)
            anchor_w = anchor_w.repeat(nB, 1).repeat(1, 1, nH*nW).view(nB*nA*nH*nW)
            anchor_h = anchor_h.repeat(nB, 1).repeat(1, 1, nH*nW).view(nB*nA*nH*nW)
            pred_boxes[0] = x.data.view(-1) + grid_x
            pred_boxes[1] = y.data.view(-1) + grid_y
            pred_boxes[2] = torch.exp(w.data.view(-1)) * anchor_w
            pred_boxes[3] = torch.exp(h.data.view(-1)) * anchor_h
            pred_boxes = convert2cpu(pred_boxes.transpose(0,1).contiguous().view(-1,4))
            t2 = time.time()
    
            nGT, nCorrect, coord_scale, tx, ty, tw, th, tconf, tcls = build_targets(pred_boxes, target.data, self.anchors, self.masked_anchors, self.anchor_mask, self.num_anchors, self.num_classes, \
                                                                   nH, nW, self.ignore_thresh, self.seen[0])
            nProposals = int((conf > 0.25).sum().data[0])
    
            tx    = tx.to(device)
            ty    = ty.to(device)
            tw    = tw.to(device)
            th    = th.to(device)
            tconf = tconf.to(device)
            tcls  = tcls.long().to(device)
    
            coord_scale = coord_scale.to(device)
    
            t3 = time.time()
    
            coord_weight = coord_scale[tconf==1]
            loss_x = F.binary_cross_entropy(x[tconf==1], tx[tconf==1], size_average=False, weight=coord_weight)
            loss_y = F.binary_cross_entropy(y[tconf==1], ty[tconf==1], size_average=False, weight=coord_weight)
            loss_w = (F.mse_loss(w[tconf==1], tw[tconf==1], size_average=False, reduce=False) * coord_weight).sum()/2.0
            loss_h = (F.mse_loss(h[tconf==1], th[tconf==1], size_average=False, reduce=False) * coord_weight).sum()/2.0
            loss_conf = F.binary_cross_entropy(conf[tconf!=-1], tconf[tconf!=-1], size_average=False)
            #loss_cls = torch.zeros(1) # F.binary_cross_entropy(cls[tcls!=-1], tcls[tcls!=-1].float(), size_average=False)
            loss_cls = F.binary_cross_entropy(cls[tcls!=-1], tcls[tcls!=-1].float(), size_average=False)
            loss = loss_x + loss_y + loss_w + loss_h + loss_conf + loss_cls
            logger.debug('ptcaffe loss_x = %f, loss_y = %f, loss_w = %f, loss_h = %f loss_conf = %f, loss_cls = %f, total = %f' % (loss_x.item(), loss_y.item(), loss_w.item(), loss_h.item(), loss_conf.item(), loss_cls.item(), loss.item()))
            t4 = time.time()
       	    if False:
                print('-----------------------------------')
                print('        activation : %f' % (t1 - t0))
                print(' create pred_boxes : %f' % (t2 - t1))
                print('     build targets : %f' % (t3 - t2))
                print('       create loss : %f' % (t4 - t3))
                print('             total : %f' % (t4 - t0))
                print('%d: nGT %d, recall %d, proposals %d, loss: x %f, y %f, w %f, h %f, conf %f, cls %f, total %f' % (self.seen[0], nGT, nCorrect, nProposals, loss_x.data[0], loss_y.data[0], loss_w.data[0], loss_h.data[0], loss_conf.data[0], loss_cls.data[0], loss.data[0]))
            self.seen[0] += nB
            return loss.view(1)
        else:
            nB = input.data.size(0)
            nA = len(self.anchor_mask)
            nC = self.num_classes
            nH = input.data.size(2)
            nW = input.data.size(3)
            output = input.clone().view(nB, nA, (5+nC), nH, nW)
            output[:, :, :2, :, :] = output[:, :, :2, :, :].sigmoid()
            output[:, :, 4:, :, :] = output[:, :, 4:, :, :].sigmoid()
            return output.view(nB,-1, nH,nW)
           # boxes = get_region_boxes(output.data, self.thresh, self.num_classes, self.masked_anchors, len(self.anchor_mask))
           # return boxes

class YoloLossWrapper(YoloLoss):
    def __init__(self, layer, *input_shapes):
        yolo_param = layer.get('yolo_param', OrderedDict()) 
        anchors = yolo_param['anchors']
        anchors = anchors.split(',')
        anchors = [float(a.strip()) for a in anchors]
        maskes = yolo_param['mask']
        maskes = maskes.split(',')
        anchor_mask = [int(m) for m in maskes]
        num_classes = int(yolo_param.get('classes', 1))
        num_anchors = int(yolo_param.get('num', 0))
        ignore_thresh = float(yolo_param.get('ignore_thresh', 0.5))
        truth_thresh = float(yolo_param.get('truth_thresh', 1.0))
        conf_thresh = float(yolo_param.get('conf_thresh',0.7))
        assert(truth_thresh == 1.0)
        stride = int(yolo_param['stride'])
        super(YoloLossWrapper, self).__init__(stride, anchor_mask, num_classes, anchors, num_anchors, ignore_thresh, truth_thresh,conf_thresh)

        # for TEST
        self.nms_thresh = float(yolo_param.get('nms_thresh', 0.4))
        self.conf_thresh = float(yolo_param.get('conf_thresh', 0.5))
        self.detect_mode = (yolo_param.get('detect_mode','false') == 'true')
    def __repr__(self):
        return 'YoloLoss()'
       
    def forward(self, *inputs):
        if self.training:
            batch_size = inputs[0].size(0)
            return YoloLoss.forward(self, *inputs)/batch_size
        else:
            if not self.detect_mode:
                return YoloLoss.forward(self, inputs[0])
            else:
                boxes = get_region_boxes(inputs[0].data, self.thresh, self.num_classes, self.masked_anchors, len(self.anchor_mask))
                return boxes

#            input = inputs[0]
#            assert(input.size(0) == 1)
#            boxes = YoloLoss.forward(self, *inputs)[0]
#            boxes = torch.FloatTensor(boxes)
#            boxes = nms(boxes, self.nms_thresh)
#            if len(boxes) > 0:
#                boxes = torch.cat(boxes, 0).view(len(boxes),-1).unsqueeze(0)
#            else:
#                boxes = torch.zeros(1, 0, 7)
#            if isinstance(input.data, torch.FloatTensor):
#                return boxes
#            else:
#                device_id = input.data.get_device()
#                return boxes.cuda(device_id)

    def forward_shape(self, *input_shapes):
        return [1,]

