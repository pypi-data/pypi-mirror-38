from __future__ import division, print_function

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from collections import OrderedDict

from ptcaffe.layer_dict import register_layer
from ptcaffe.utils.utils import make_list

def fast_hist(a, b, n):
    k = (a >= 0) & (a < n)
    return np.bincount(n * a[k].astype(int) + b[k], minlength=n**2).reshape(n, n)

@register_layer('SegAccuracy')
class SegAccuracy(nn.Module):
    def __init__(self, layer, *input_shapes):
        super(SegAccuracy, self).__init__()

        seg_accuracy_param = layer.get('seg_accuracy_param', OrderedDict())
        ignore_label = seg_accuracy_param.get('ignore_label', None)
        self.ignore_label = int(ignore_label) if ignore_label is not None else None
        self.tnames = make_list(layer['top'])

    def forward_shape(self, *input_shapes):
        if len(self.tnames) == 1:
            return [3,]
        else:
            return [1,], [1,], [1,]

    def __repr__(self):
        return "SegAccuracy()"

    def forward(self, pred, label):
        num_classes = pred.size(1)
        device = pred.device
        pred = pred.transpose(0,1).contiguous().view(num_classes,-1).transpose(0,1).contiguous()
        _, pred = pred.max(1)
        pred = pred.cpu().numpy()
        gt = label.cpu().view(-1).long().numpy()

        if self.ignore_label is not None:
            pred = pred[gt != self.ignore_label]
            gt = gt[gt != self.ignore_label]

        hist = fast_hist(gt, pred, num_classes)

        eps = 1e-6
        hist_sum = float(hist.sum())

        hist_colsum = hist.sum(1).astype('float32')

        hist_union = (hist.sum(1) + hist.sum(0) - np.diag(hist)).astype('float32')

        # results
        accuracy = np.diag(hist).sum() / hist_sum

        recalls = np.diag(hist).copy()
        recalls = recalls[hist_colsum > 0]
        recalls = recalls / hist_colsum[hist_colsum > 0]
        avgRecall = np.sum(recalls)/len(recalls)

        mious = np.diag(hist).copy()
        mask = (mious == hist_union)
        mious[mask] = 1.0
        hist_union[mask] = 1.0
        mious = mious / hist_union
        avgJaccard = np.sum(mious)/len(mious)

        if len(self.tnames) == 1:
            output = torch.FloatTensor([accuracy, avgRecall, avgJaccard]).to(device)
            return output
        elif len(self.tnames) == 3:
            accuracy = torch.FloatTensor([accuracy,]).to(device)
            avgRecall = torch.FloatTensor([avgRecall,]).to(device)
            avgJaccard = torch.FloatTensor([avgJaccard,]).to(device)
            return accuracy, avgRecall, avgJaccard
        else:
            assert(False)

