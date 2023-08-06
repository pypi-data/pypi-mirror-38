import time
import torch
import math
import torch.nn as nn
import torch.nn.functional as F
from .utils import *
from ptcaffe.utils.config import cfg
from collections import OrderedDict

def build_targets(pred_boxes, target, anchors, num_anchors, num_classes, nH, nW, noobject_scale, object_scale, sil_thresh, seen):
    nB = target.size(0)
    nA = num_anchors
    nC = num_classes
    anchor_step = len(anchors)/num_anchors
    conf_mask  = torch.ones(nB, nA, nH, nW) * noobject_scale
    coord_mask = torch.zeros(nB, nA, nH, nW)
    cls_mask   = torch.zeros(nB, nA, nH, nW)
    tx         = torch.zeros(nB, nA, nH, nW) 
    ty         = torch.zeros(nB, nA, nH, nW) 
    tw         = torch.zeros(nB, nA, nH, nW) 
    th         = torch.zeros(nB, nA, nH, nW) 
    tconf      = torch.zeros(nB, nA, nH, nW)
    tcls       = torch.zeros(nB, nA, nH, nW) 

    nAnchors = nA*nH*nW
    nPixels  = nH*nW
    for b in xrange(nB):
        cur_pred_boxes = pred_boxes[b*nAnchors:(b+1)*nAnchors].t()
        cur_ious = torch.zeros(nAnchors)
        for t in xrange(target.shape[1]//5):
            if target[b][t*5+1] == 0:
                break
            gx = target[b][t*5+1]*nW
            gy = target[b][t*5+2]*nH
            gw = target[b][t*5+3]*nW
            gh = target[b][t*5+4]*nH
            cur_gt_boxes = torch.FloatTensor([gx,gy,gw,gh]).repeat(nAnchors,1).t()
            cur_ious = torch.max(cur_ious, bbox_ious(cur_pred_boxes, cur_gt_boxes, x1y1x2y2=False))
        conf_mask[b][(cur_ious>sil_thresh).view(num_anchors, nH, nW)] = 0
    if False: #seen < 12800:
       if anchor_step == 4:
           tx = torch.FloatTensor(anchors).view(nA, anchor_step).index_select(1, torch.LongTensor([2])).view(1,nA,1,1).repeat(nB,1,nH,nW)
           ty = torch.FloatTensor(anchors).view(num_anchors, anchor_step).index_select(1, torch.LongTensor([2])).view(1,nA,1,1).repeat(nB,1,nH,nW)
       else:
           tx.fill_(0.5)
           ty.fill_(0.5)
       tw.zero_()
       th.zero_()
       coord_mask.fill_(1)

    nGT = 0
    nCorrect = 0
    for b in xrange(nB):
        for t in xrange(target.shape[1]//5):
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
            for n in xrange(nA):
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
                    if anchor_step == 4:
                        min_dist = dist
                elif anchor_step==4 and iou == best_iou and dist < min_dist:
                    best_iou = iou
                    best_n = n
                    min_dist = dist

            gt_box = [gx, gy, gw, gh]
            pred_box = pred_boxes[b*nAnchors+best_n*nPixels+gj*nW+gi]

            coord_mask[b][best_n][gj][gi] = 1 # 2 - gw*gh/(nW*nH)
            cls_mask[b][best_n][gj][gi] = 1
            conf_mask[b][best_n][gj][gi] = object_scale
            tx[b][best_n][gj][gi] = target[b][t*5+1] * nW - gi
            ty[b][best_n][gj][gi] = target[b][t*5+2] * nH - gj
            tw[b][best_n][gj][gi] = math.log(gw/anchors[anchor_step*best_n])
            th[b][best_n][gj][gi] = math.log(gh/anchors[anchor_step*best_n+1])
            iou = bbox_iou(gt_box, pred_box, x1y1x2y2=False) # best_iou
            tconf[b][best_n][gj][gi] = iou
            tcls[b][best_n][gj][gi] = target[b][t*5]
            if iou > 0.5:
                nCorrect = nCorrect + 1

    return nGT, nCorrect, coord_mask, conf_mask, cls_mask, tx, ty, tw, th, tconf, tcls

class RegionLoss(nn.Module):
    def __init__(self, num_classes=0, anchors=[], num_anchors=1):
        super(RegionLoss, self).__init__()
        self.num_classes = num_classes
        self.anchors = anchors
        self.num_anchors = num_anchors
        self.anchor_step = len(anchors)/num_anchors
        self.coord_scale = 1
        self.noobject_scale = 1
        self.object_scale = 5
        self.class_scale = 1
        self.thresh = 0.6
        self.seen = [0]

    def forward(self, input, target=None):
        if self.training:
            #input : BxAs*(4+1+num_classes)*H*W
            t0 = time.time()
            nB = input.data.size(0)
            nA = self.num_anchors
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
            cls  = output.index_select(2, torch.linspace(5,5+nC-1,nC).long().to(device))
            cls  = cls.view(nB*nA, nC, nH*nW).transpose(1,2).contiguous().view(nB*nA*nH*nW, nC)
            t1 = time.time()
    
            pred_boxes = torch.FloatTensor(4, nB*nA*nH*nW).to(device)
            grid_x = torch.linspace(0, nW-1, nW).repeat(nH,1).repeat(nB*nA, 1, 1).view(nB*nA*nH*nW).to(device)
            grid_y = torch.linspace(0, nH-1, nH).repeat(nW,1).t().repeat(nB*nA, 1, 1).view(nB*nA*nH*nW).to(device)
            anchor_w = torch.Tensor(self.anchors).view(nA, self.anchor_step).index_select(1, torch.LongTensor([0])).to(device)
            anchor_h = torch.Tensor(self.anchors).view(nA, self.anchor_step).index_select(1, torch.LongTensor([1])).to(device)
            anchor_w = anchor_w.repeat(nB, 1).repeat(1, 1, nH*nW).view(nB*nA*nH*nW)
            anchor_h = anchor_h.repeat(nB, 1).repeat(1, 1, nH*nW).view(nB*nA*nH*nW)
            pred_boxes[0] = x.data.view(-1) + grid_x
            pred_boxes[1] = y.data.view(-1) + grid_y
            pred_boxes[2] = torch.exp(w.data.view(-1)) * anchor_w
            pred_boxes[3] = torch.exp(h.data.view(-1)) * anchor_h
            pred_boxes = convert2cpu(pred_boxes.transpose(0,1).contiguous().view(-1,4))
            t2 = time.time()
    
            nGT, nCorrect, coord_mask, conf_mask, cls_mask, tx, ty, tw, th, tconf,tcls = build_targets(pred_boxes, target.data, self.anchors, nA, nC, \
                                                                   nH, nW, self.noobject_scale, self.object_scale, self.thresh, self.seen[0])
            cls_mask = (cls_mask == 1)
            nProposals = int((conf > 0.25).sum().data[0])
    
            tx    = tx.to(device)
            ty    = ty.to(device)
            tw    = tw.to(device)
            th    = th.to(device)
            tconf = tconf.to(device)
            tcls  = tcls[cls_mask].long().to(device)
    
            coord_mask = coord_mask.to(device).sqrt()
            conf_mask  = conf_mask.to(device).sqrt()
            cls_mask   = cls_mask.view(-1, 1).repeat(1,nC).to(device)
            cls        = cls[cls_mask].view(-1, nC)  
    
            t3 = time.time()
    
            loss_x = self.coord_scale * nn.MSELoss(size_average=False)(x*coord_mask, tx*coord_mask)/2.0
            loss_y = self.coord_scale * nn.MSELoss(size_average=False)(y*coord_mask, ty*coord_mask)/2.0
            loss_w = self.coord_scale * nn.MSELoss(size_average=False)(w*coord_mask, tw*coord_mask)/2.0
            loss_h = self.coord_scale * nn.MSELoss(size_average=False)(h*coord_mask, th*coord_mask)/2.0
            loss_conf = nn.MSELoss(size_average=False)(conf*conf_mask, tconf*conf_mask)/2.0
            loss_cls = self.class_scale * nn.CrossEntropyLoss(size_average=False)(cls, tcls)
            loss = loss_x + loss_y + loss_w + loss_h + loss_conf + loss_cls
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
            nA = self.num_anchors
            nC = self.num_classes
            nH = input.data.size(2)
            nW = input.data.size(3)
            output = input.clone().view(nB, nA, (5+nC), nH, nW)
            output[:, :, :2, :, :] = output[:, :, :2, :, :].sigmoid()
            output[:, :, 4, :, :] = output[:, :, 4, :, :].sigmoid()
            output[:, :, 5:, :, :] = F.softmax(output[:, :, 5:, :, :], dim=2)
            return output.view(nB,-1, nH,nW)


class RegionLossWrapper(RegionLoss):
    def __init__(self, layer, *input_shapes):
        region_param = layer.get('region_param', OrderedDict()) 
        anchors = region_param.get('anchors')
        anchors = anchors.split(',')
        self.anchors = [float(a.strip()) for a in anchors]
        self.num_classes = int(region_param.get('classes', 1))
        self.num_anchors = int(region_param.get('num', 0))
        super(RegionLossWrapper, self).__init__(self.num_classes, self.anchors, self.num_anchors)
        self.coord_scale = float(region_param.get('coord_scale', 1))
        self.noobject_scale = float(region_param.get('noobject_scale', 1))
        self.object_scale = float(region_param.get('object_scale', 5))
        self.class_scale = float(region_param.get('class_scale', 1))
        self.thresh = float(region_param.get('conf_thresh', 0.6))
        self.detect_mode = (region_param.get('detect_mode', 'false') == 'true')

        # for TEST
        self.nms_thresh = float(region_param.get('nms_thresh', 0.4))
        self.conf_thresh = float(region_param.get('conf_thresh', 0.5))

    def __repr__(self):
        return 'RegionLoss()'

    def forward(self, *inputs):
        if self.training:
            batch_size = inputs[0].size(0)
            return RegionLoss.forward(self, *inputs)/batch_size
        else:
            if not self.detect_mode:
                return RegionLoss.forward(self, inputs[0])
            else:
                input = inputs[0]
                assert(input.size(0) == 1)
                boxes = get_region_boxes(input.data, self.conf_thresh, self.num_classes, self.anchors, self.num_anchors, 1, 0)[0]
                boxes = torch.FloatTensor(boxes)
                boxes = nms(boxes, self.nms_thresh)
                if len(boxes) > 0:
                    boxes = torch.cat(boxes, 0).view(len(boxes),-1)
                else:
                    boxes = torch.zeros(0, 7)
                if isinstance(input.data, torch.FloatTensor):
                    return boxes
                else:
                    device_id = input.data.get_device()
                    return boxes.cuda(device_id)

    def forward_shape(self, *input_shapes):
        return [1,]
