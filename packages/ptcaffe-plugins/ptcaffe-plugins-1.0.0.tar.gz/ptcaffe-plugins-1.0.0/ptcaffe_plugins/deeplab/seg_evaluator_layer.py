from __future__ import division, print_function

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from collections import OrderedDict

from ptcaffe.layer_dict import register_layer, BaseEvaluator

# reference from : https://github.com/hualin95/Deeplab-v3plus/blob/master/utils/eval.py
class SegEvalMetric(object):
    def __init__(self, num_classes):
        self.num_classes = num_classes
        self.reset()

    def update(self, pre_image, gt_image):
        assert gt_image.shape == pre_image.shape
        mask = (gt_image >= 0) & (gt_image < self.num_classes)
        label = self.num_classes * gt_image[mask].astype('int') + pre_image[mask]
        count = np.bincount(label, minlength=self.num_classes**2)
        confusion_matrix = count.reshape(self.num_classes, self.num_classes)
        self.confusion_matrix += confusion_matrix

    def reset(self):
        self.confusion_matrix = np.zeros((self.num_classes,) * 2)

    def get(self):
        if np.sum(self.confusion_matrix) == 0:
            print("Attention: pixel_total is zero!!!")
            PA = 0
        else:
            PA = np.diag(self.confusion_matrix).sum() / self.confusion_matrix.sum()

        MPA = np.diag(self.confusion_matrix) / self.confusion_matrix.sum(axis=1)
        MPA = np.nanmean(MPA)

        MIoU = np.diag(self.confusion_matrix) / (
                    np.sum(self.confusion_matrix, axis=1) + np.sum(self.confusion_matrix, axis=0) -
                    np.diag(self.confusion_matrix))
        MIoU = np.nanmean(MIoU)


        FWIoU = np.multiply(np.sum(self.confusion_matrix, axis=1), np.diag(self.confusion_matrix))
        FWIoU = FWIoU / (np.sum(self.confusion_matrix, axis=1) + np.sum(self.confusion_matrix, axis=0) - np.diag(self.confusion_matrix))
        FWIoU = np.sum(i for i in FWIoU if not np.isnan(i)) / np.sum(self.confusion_matrix)

        return {'PA': PA, 'MPA': MPA, 'MIoU': MIoU, 'FWIoU': FWIoU}

@register_layer('SegEvaluator')
class SegEvaluator(BaseEvaluator):
    def __init__(self, layer, *input_shapes):
        super(SegEvaluator, self).__init__(layer, *input_shapes)

    def create_metric(self, layer, *input_shapes):
        evaluator_param = layer.get('evaluator_param', OrderedDict())
        num_classes = int(evaluator_param['num_classes'])
        metric = SegEvalMetric(num_classes)
        return metric

    def forward(self, score, label):
        pred = score.cpu().numpy()
        label = label.squeeze(1).cpu().numpy()
        argpred = np.argmax(pred, axis=1)

        self.lock.acquire()
        self.metric.update(argpred, label)
        self.lock.release()

    def __repr__(self):
        return 'SegEvaluator()'

