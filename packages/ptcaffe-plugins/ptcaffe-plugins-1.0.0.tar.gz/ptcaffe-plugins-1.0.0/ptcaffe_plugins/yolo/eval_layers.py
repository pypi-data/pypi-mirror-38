import os
import torch
import torch.nn as nn
from .utils import bbox_iou, get_region_boxes, get_image_size, nms
from ptcaffe.utils.utils import ThreadsSync
from collections import OrderedDict
from easydict import EasyDict as edict
import copy
from voc_eval import _do_python_eval
from ptcaffe.utils.config import cfg

class Yolov2Recall(nn.Module):
    def __init__(self, layer, *input_shapes):
        super(Yolov2Recall, self).__init__()
        region_param = layer.get('region_param', OrderedDict())
        recall_param = layer.get('recall_param', OrderedDict())

        anchors = region_param.get('anchors')
        anchors = anchors.split(',')
        self.anchors = [float(a.strip()) for a in anchors]
        self.num_classes = int(region_param.get('classes', 1))
        self.num_anchors = int(region_param.get('num', 0))

        # for recall 
        self.nms_thresh = float(recall_param.get('nms_thresh', 0.45))
        self.conf_thresh = float(recall_param.get('conf_thresh', 0.5))
        self.iou_thresh = float(recall_param.get('iou_thresh', 0.5))
        self.max_iter = int(recall_param['max_iter'])

        self.cur_device = -1
        self.device_ids = [0]

        self.fps = [0] * self.num_classes
        
        self.seen = dict()
        for idx, dev in enumerate(self.device_ids):
            assert(idx == dev)
            self.seen[dev] = 0

        # for synchronize
        self.sync = ThreadsSync()

        self.eval = edict()
        self.eval.total = 0
        self.eval.proposals = 0
        self.eval.correct = 0
        
    def __repr__(self):
        return 'Yolov2Recall()'

    def set_device(self, cur_device):
        self.cur_device = cur_device

    def set_devices(self, device_ids):
        self.device_ids = copy.copy(device_ids)
        if len(self.device_ids) > 1:
            for idx, dev in enumerate(self.device_ids):
                assert(idx == dev)
                self.seen[dev] = 0
        else:
            device = self.device_ids[0]
            self.seen[device] = 0

    def forward(self, *inputs):
        def truths_length(truths):
            for i in range(truths.shape[1]//5):
                if truths[i][1] == 0:
                    return i

        output = inputs[0].data
        device = self.cur_device
        assert(device == output.get_device())

        target = inputs[1].data
        all_boxes = get_region_boxes(output, self.conf_thresh, self.num_classes, self.anchors, self.num_anchors)
        for i in range(output.size(0)):
            boxes = all_boxes[i]
            boxes = nms(boxes, self.nms_thresh)
            truths = target[i].view(-1, 5)
            num_gts = truths_length(truths)
     
            self.eval.total += num_gts
    
            for i in range(len(boxes)):
                if boxes[i][4] > self.conf_thresh:
                    self.eval.proposals += 1

            for i in range(num_gts):
                box_gt = [truths[i][1], truths[i][2], truths[i][3], truths[i][4], 1.0, 1.0, truths[i][0]]
                best_iou = 0
                best_j = -1
                for j in range(len(boxes)):
                    iou = bbox_iou(box_gt, boxes[j], x1y1x2y2=False)
                    if iou > best_iou:
                        best_j = j
                        best_iou = iou
                if best_iou > self.iou_thresh: # and boxes[best_j][6] == box_gt[6]:
                    self.eval.correct += 1

        self.seen[device] += 1
        if cfg.VERBOSE_LEVEL >= 2:
            print('[%d] seen = %d' % (device, self.seen[device]))

        if len(self.device_ids) == 1 and self.seen[device] % 5 == 0:
            eps = 1e-6
            precision = 1.0*self.eval.correct/(self.eval.proposals+eps)
            recall = 1.0*self.eval.correct/(self.eval.total+eps)
            fscore = 2.0*precision*recall/(precision+recall+eps)
            if cfg.VERBOSE_LEVEL >= 2:
                print("%d precision: %f, recall: %f, fscore: %f" % (self.seen[device], precision, recall, fscore))

        if self.seen[device] == self.max_iter:
            if len(self.device_ids) == 1 or device == 0:
                for i in self.device_ids:
                    self.seen[i] = 0
                
                eps = 1e-6
                precision = 1.0*self.eval.correct/(self.eval.proposals+eps)
                recall = 1.0*self.eval.correct/(self.eval.total+eps)
                fscore = 2.0*precision*recall/(precision+recall+eps)
                self.eval.correct = 0
                print("precision: %f, recall: %f, fscore: %f" % (precision, recall, fscore))

                self.eval.total = 0
                self.eval.proposals = 0
                self.eval.correct = 0
            if cfg.VERBOSE_LEVEL >= 2:
                print('[%d] test_finished' % device)
            self.sync.wait_synchronize(len(self.device_ids)) # very necessary here, otherwise error will happen

    def forward_shape(self, *input_shapes):
        return

#@register_layer('YoloDetectionOutput')
#class YoloDetectionOutput(nn.Module):
#    def __init__(self, layer, input_shape):
#        super(YoloDetectionOutput, self).__init__()
#
#@register_layer('YoloDetectionEvaluate'):
#class YoloDetectionEvaluate(BaseEvaluator):
#    def __init__(self, layer, *input_shapes):
#        super(YoloDetectionEvaluate, self).__init__(layer, *input_shapes)
#
#    def create_metric(self, layer, *input_shapes):
#        return
    

#@register_layer('Yolov3Valid_VOC')
#class Yolov3Valid_VOC(nn.Module):
#    def __init__(self, layer, *input_shapes):
#        super(Yolov3Valid_VOC, self).__init__()
#        yolo_params = layer['yolo_param']
#        valid_param = layer.get('valid_param', OrderedDict())
#
#        self.stride = []
#        self.anchors = []
#        self.num_classes = []
#        self.num_anchors = []
#        for yolo_param in yolo_params:
#            anchors = yolo_param.get('anchors')
#            anchors = anchors.split(',')
#            anchors = [float(a.strip()) for a in anchors]
#
#            maskes = yolo_param['mask']
#            maskes = maskes.split(',')
#            anchor_mask = [int(m) for m in maskes]
#            stride = int(yolo_param['stride'])
#            anchors = [anchor/stride for anchor in anchors]
#            masked_anchors = []
#            for m in anchor_mask:
#                masked_anchors += anchors[m*2:(m+1)*2]
#
#            self.stride.append(stride)
#            self.anchors.append(masked_anchors)
#            self.num_classes.append(int(yolo_param.get('classes', 1)))
#            self.num_anchors.append(len(maskes))
#
#        self.conf_thresh = float(valid_param.get('conf_thresh', 0.005))
#        self.nms_thresh = float(valid_param.get('nms_thresh', 0.45))
#        self.max_iter = int(valid_param['max_iter'])
#        self.valid_gt = valid_param['valid']
#
#        self.cur_device = -1
#        self.device_ids = [0]
#        with open(self.valid_gt) as fp:
#            tmp_files = fp.readlines()
#            self.valid_files = [item.rstrip() for item in tmp_files]
#
#        self.fps = [0] * self.num_classes[0]
#        self.save_dir = valid_param['save_dir']
#        self.output_dir = valid_param['output_dir']
#        self.prefix = 'comp4_det_test_'
#        if not os.path.exists(self.save_dir):
#            os.mkdir(self.save_dir)
#        if not os.path.exists(self.output_dir):
#            os.mkdir(self.output_dir)
#        self.names = valid_param['names'].split(',')
#        assert(len(self.names) == self.num_classes[0])
#        
#        self.seen = dict()
#        for idx, dev in enumerate(self.device_ids):
#            assert(idx == dev)
#            self.seen[dev] = 0
#
#        # for synchronize_here
#        self.sync0 = ThreadsSync()
#        self.sync1 = ThreadsSync()
#
#    def __repr__(self):
#        return 'Yolov3Valid_VOC()'
#
#    def set_device(self, cur_device):
#        self.cur_device = cur_device
#
#    def set_devices(self, device_ids):
#        self.device_ids = copy.copy(device_ids)
#        if len(self.device_ids) > 1:
#            for idx, dev in enumerate(self.device_ids):
#                assert(idx == dev)
#                self.seen[dev] = 0
#        else:
#            device = self.device_ids[0]
#            self.seen[device] = 0
#
#    def forward(self, *inputs):
#        assert(len(inputs) == 3)
#        device = self.cur_device
#        assert(device == inputs[0].data.get_device())
#
#        # init fps
#        if self.seen[device] == 0:
#            if len(self.device_ids) == 1 or device == 0:
#                print('init fps')
#                for i in range(self.num_classes[0]):
#                    buf = '%s/%s%s.txt' % (self.save_dir, self.prefix, self.names[i])
#                    self.fps[i] = open(buf, 'w')
#            self.sync0.wait_synchronize(len(self.device_ids))
#
#        assert(len(inputs) == 3)
#        batch_boxes0 = get_region_boxes(inputs[0].data, self.conf_thresh, self.num_classes[0], self.anchors[0], self.num_anchors[0], 0, 1)
#        batch_boxes1 = get_region_boxes(inputs[1].data, self.conf_thresh, self.num_classes[1], self.anchors[1], self.num_anchors[1], 0, 1)
#        batch_boxes2 = get_region_boxes(inputs[2].data, self.conf_thresh, self.num_classes[2], self.anchors[2], self.num_anchors[2], 0, 1)
#        batch_size = inputs[0].size(0) 
#        for i in range(batch_size):
#            num_gpus = len(self.device_ids)
#            lineId = self.seen[device] * batch_size * num_gpus + device * batch_size + i
#            fileId = os.path.basename(self.valid_files[lineId]).split('.')[0]
#            width, height = get_image_size(self.valid_files[lineId])
#            #print(self.valid_files[lineId])
#            boxes = batch_boxes0[i] + batch_boxes1[i] + batch_boxes2[i]
#            boxes = nms(boxes, self.nms_thresh)
#            for box in boxes:
#                x1 = (box[0] - box[2]/2.0) * width
#                y1 = (box[1] - box[3]/2.0) * height
#                x2 = (box[0] + box[2]/2.0) * width
#                y2 = (box[1] + box[3]/2.0) * height
#
#                det_conf = box[4]
#                for j in range((len(box)-5)/2):
#                    cls_conf = box[5+2*j]
#                    cls_id = box[6+2*j]
#                    prob =det_conf * cls_conf
#                    self.fps[cls_id].write('%s %f %f %f %f %f\n' % (fileId, prob, x1, y1, x2, y2))
#
#        self.seen[device] += 1
#        print('device %d, seen = %d' % (device, self.seen[device]))
#
#        # close fps
#        if self.seen[device] == self.max_iter:
#            self.sync1.wait_synchronize(len(self.device_ids))
#            if len(self.device_ids) == 1 or device == 0:
#                for i in self.device_ids:
#                    self.seen[i] = 0
#                print('close fps')
#                for i in range(self.num_classes[0]):
#                    self.fps[i].close()
#                import pytorch_yolo2.scripts.voc_eval as voc_eval
#                voc_eval._do_python_eval("%s/%s" % (self.save_dir, self.prefix), output_dir=self.output_dir)
#
#    def forward_shape(self, *input_shapes):
#        return


class Yolov2Valid(nn.Module):
    def __init__(self, layer, *input_shapes):
        super(Yolov2Valid, self).__init__()
        region_param = layer.get('region_param', OrderedDict())
        valid_param = layer.get('valid_param', OrderedDict())

        anchors = region_param.get('anchors')
        anchors = anchors.split(',')
        self.anchors = [float(a.strip()) for a in anchors]
        self.num_classes = int(region_param.get('classes', 1))
        self.num_anchors = int(region_param.get('num', 0))

        # for Valid
        self.nms_thresh = float(valid_param.get('nms_thresh', 0.45))
        self.conf_thresh = float(valid_param.get('conf_thresh', 0.005))
        self.iou_thresh = float(valid_param.get('iou_thresh', 0.5))
        self.max_iter = int(valid_param['max_iter'])

        self.valid_gt = valid_param['valid']
        self.cur_device = -1
        self.device_ids = [0]
        with open(self.valid_gt) as fp:
            tmp_files = fp.readlines()
            self.valid_files = [item.rstrip() for item in tmp_files]

        self.fps = [0] * self.num_classes
        self.save_dir = valid_param['save_dir']
        self.output_dir = valid_param['output_dir']
        self.prefix = 'comp4_det_test_'
        if not os.path.exists(self.save_dir):
            os.mkdir(self.save_dir)
        if not os.path.exists(self.output_dir):
            os.mkdir(self.output_dir)
        self.names = valid_param['names'].split(',')
        assert(len(self.names) == self.num_classes)
        
        self.seen = dict()
        for idx, dev in enumerate(self.device_ids):
            assert(idx == dev)
            self.seen[dev] = 0

        # for synchronize
        self.sync0 = ThreadsSync()
        self.sync1 = ThreadsSync()

    def __repr__(self):
        return 'Yolov2Valid()'

    def set_device(self, cur_device):
        self.cur_device = cur_device

    def set_devices(self, device_ids):
        self.device_ids = copy.copy(device_ids)
        if len(self.device_ids) > 1:
            for idx, dev in enumerate(self.device_ids):
                assert(idx == dev)
                self.seen[dev] = 0
        else:
            device = self.device_ids[0]
            self.seen[device] = 0

    def forward(self, *inputs):
        output = inputs[0].data
        device = self.cur_device 
        assert(device == output.get_device())

        # init fps
        if self.seen[device] == 0:
            if len(self.device_ids) == 1 or device == 0:
                print('init fps')
                for i in range(self.num_classes):
                    buf = '%s/%s%s.txt' % (self.save_dir, self.prefix, self.names[i])
                    self.fps[i] = open(buf, 'w')
            self.sync0.wait_synchronize(len(self.device_ids))

        batch_boxes = get_region_boxes(output, self.conf_thresh, self.num_classes, self.anchors, self.num_anchors, 0, 1)
        batch_size = output.size(0) 
        for i in range(output.size(0)):
            num_gpus = len(self.device_ids)
            lineId = self.seen[device] * batch_size * num_gpus + device * batch_size + i
            fileId = os.path.basename(self.valid_files[lineId]).split('.')[0]
            width, height = get_image_size(self.valid_files[lineId])
            #print(self.valid_files[lineId])
            boxes = batch_boxes[i]
            boxes = nms(boxes, self.nms_thresh)
            for box in boxes:
                x1 = (box[0] - box[2]/2.0) * width
                y1 = (box[1] - box[3]/2.0) * height
                x2 = (box[0] + box[2]/2.0) * width
                y2 = (box[1] + box[3]/2.0) * height

                det_conf = box[4]
                for j in range((len(box)-5)/2):
                    cls_conf = box[5+2*j]
                    cls_id = box[6+2*j]
                    prob =det_conf * cls_conf
                    self.fps[cls_id].write('%s %f %f %f %f %f\n' % (fileId, prob, x1, y1, x2, y2))

        self.seen[device] += 1
        if cfg.VERBOSE_LEVEL >= 2:
            print('device %d, seen = %d' % (device, self.seen[device]))

        # close fps
        if self.seen[device] == self.max_iter:
            self.sync1.wait_synchronize(len(self.device_ids))
            if len(self.device_ids) == 1 or device == 0:
                for i in self.device_ids:
                    self.seen[i] = 0
                print('close fps')
                for i in range(self.num_classes):
                    self.fps[i].close()
                _do_python_eval("%s/%s" % (self.save_dir, self.prefix), output_dir=self.output_dir)

    def forward_shape(self, *input_shapes):
        return

