from __future__ import division, print_function

import threading
import torch
import torch.nn as nn
import numpy as np

from collections import OrderedDict
from ptcaffe.layer_dict import register_layer
from ptcaffe.utils.logger import logger

@register_layer('DetectionEvaluate')
class DetectionEvaluate(nn.Module):
    def __init__(self, layer, *input_shapes):
        super(DetectionEvaluate, self).__init__()
        detection_evaluate_param = layer.get('detection_evaluate_param', OrderedDict())
        self.background_label_id = int(detection_evaluate_param.get('background_label_id', 0))
       	assert(self.background_label_id == 0)
        self.overlap_threshold = float(detection_evaluate_param.get('overlap_threshold', 0.5))
        self.evaluate_difficult_gt = (detection_evaluate_param.get('evaluate_difficult_gt', 'false') == 'true')

        if 'classes_type' in detection_evaluate_param:
            classes_type = detection_evaluate_param['classes_type']
            if classes_type == 'pascal':
                self.classes = DetectionOutput.VOC_CLASSES
            elif classes_type == 'pedface':
                self.classes = DetectionOutput.PEDFACE_CLASSES
            else:
                assert False
        elif 'classes' in detection_evaluate_param:
            self.classes = detection_evaluate_param['classes'].split(',')
            self.classes = list(map(lambda x: x.strip(), self.classes))
        else:
            self.classes = None

        if self.classes is None:
            self.num_classes = int(detection_evaluate_param['num_classes'])
            self.classes = ['class%d' % i for i in range(self.num_classes)]
        else:
            self.num_classes = len(self.classes)

        from .voc_detection import VOC07MApMetric, VOCMApMetric
        self.use_07_metric = (detection_evaluate_param.get('use_07_metric', 'false') == 'true')

        if self.use_07_metric:
            self.metric = VOC07MApMetric(iou_thresh=self.overlap_threshold, class_names=self.classes)
        else:
            self.metric = VOCMApMetric(iou_thresh=self.overlap_threshold, class_names=self.classes)

        self.lock = threading.Lock()
        self.device = -1
        self.devices = [-1]

    def set_device(self, device):
        self.device = device

    def set_devices(self, devices):
        self.devices = devices

    def reset_metric(self):
        if self.device == self.devices[0]:
            mAP = self.metric.get()
            for k, v in zip(*mAP):
                logger.info('{}: {}'.format(k, v))
            self.metric.reset()

    def forward_shape(self, *input_shapes):
        return

    def forward(self, detection_out, label):
        #  import pdb; pdb.set_trace()
        detection_out = detection_out[0, 0]
        label = label[0, 0]
        if detection_out.is_cuda:
            detection_out = detection_out.data.cpu().numpy()
            label = label.data.cpu().numpy()
        else:
            detection_out = detection_out.data.numpy()
            label = label.data.numpy()

        B = int(max(max(detection_out[:, 0]), max(label[:, 0])) + 1)
        N = 0
        M = 0
        bboxes_list = []
        scores_list = []
        labels_list = []
        gt_bboxes_list = []
        gt_labels_list = []
        gt_difficults_list = []

        for batch_id in xrange(B):
            img_preds = detection_out[detection_out[:, 0] == batch_id]
            N = max(N, img_preds.shape[0])
            bboxes_list.append(img_preds[:, 3:])
            scores_list.append(img_preds[:, 2])
            labels_list.append(img_preds[:, 1])

            img_gt_labels = label[label[:, 0] == batch_id]
            M = max(M, img_gt_labels.shape[0])
            gt_bboxes_list.append(img_gt_labels[:, 3:7])
            gt_labels_list.append(img_gt_labels[:, 1])
            if self.evaluate_difficult_gt:
                gt_difficults_list.append(img_gt_labels[:, 7] * 0)
            else:
                gt_difficults_list.append(img_gt_labels[:, 7])

        pred_bboxes = np.zeros((B, N, 4), dtype=np.float32)
        pred_scores = np.zeros((B, N), dtype=np.float32)
        pred_labels = np.zeros((B, N), dtype=np.int32)
        for i, (bboxes, scores, labels) in enumerate(zip(bboxes_list, scores_list, labels_list)):
            n_box = bboxes.shape[0]
            if True: # N > n_box:
                pred_labels[i] = np.concatenate((labels, np.full((N - n_box), -1)))
                pred_scores[i] = np.concatenate((scores, np.zeros((N - n_box))))
                pred_bboxes[i] = np.concatenate((bboxes, np.zeros((N - n_box, 4))))

        gt_bboxes = np.zeros((B, M, 4), dtype=np.float32)
        gt_labels = np.zeros((B, M), dtype=np.int32)
        gt_difficults = np.zeros((B, M), dtype=np.float32)
        for i, (bboxes, labels, difficults) in enumerate(zip(gt_bboxes_list, gt_labels_list, gt_difficults_list)):
            n_box = bboxes.shape[0]
            if True: #M > n_box:
                gt_labels[i] = np.concatenate((labels, np.full((M - n_box), -1)))
                gt_difficults[i] = np.concatenate((difficults, np.zeros((M - n_box))))
                gt_bboxes[i] = np.concatenate((bboxes, np.zeros((M - n_box, 4))))

        #  import pdb; pdb.set_trace()
        self.lock.acquire()
        self.metric.update(pred_bboxes, pred_labels, pred_scores, gt_bboxes, gt_labels, gt_difficults)
        self.lock.release()

    def __repr__(self):
        return "DetectionEvaluate()"
