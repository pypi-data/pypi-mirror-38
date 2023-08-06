from __future__ import division, print_function

import numpy as np
import torch
import torch.nn as nn

from ptcaffe.layer_dict import register_layer


def _fast_hist(label_true, label_pred, n_class):
    mask = (label_true >= 0) & (label_true < n_class)
    hist = np.bincount(
        n_class * label_true[mask].astype(int) +
        label_pred[mask], minlength=n_class ** 2).reshape(n_class, n_class)
    return hist

class ScoreMetric(object):
    def __init__(self, n_class):
        self.hist = np.zeros((n_class, n_class))
        self.n_class = n_class

    def reset(self):
        self.hist = np.zeros((self.n_class, self.n_class))

    def update(self, score, target):
        lbl_pred = score.data.max(1)[1].cpu().numpy()[:, :, :]
        lbl_true = target.data.cpu()
        for lt, lp in zip(lbl_true, lbl_pred):
            lt = lt.numpy()
            self.hist += _fast_hist(lt.flatten(), lp.flatten(), self.n_class)

    def get(self):
        hist = self.hist
        acc = np.diag(hist).sum() / hist.sum()
        acc_cls = np.diag(hist) / hist.sum(axis=1)
        acc_cls = np.nanmean(acc_cls)
        iu = np.diag(hist) / (hist.sum(axis=1) + hist.sum(axis=0) - np.diag(hist))
        mean_iu = np.nanmean(iu)
        freq = hist.sum(axis=1) / hist.sum()
        fwavacc = (freq[freq > 0] * iu[freq > 0]).sum()
        return acc, acc_cls, mean_iu, fwavacc

@register_layer('ScoreEvaluator')
class ScoreEvaluator(nn.Module):
    def __init__(self, layer, *input_shapes):
        super(ScoreEvaluator, self).__init__()
        self.num_classes = int(layer['evaluator_param']['num_classes'])
        self.metric = ScoreMetric(self.num_classes)

    def __repr__(self):
        return "ScoreEvaluator()"

    def reset_metric(self):
        metrics = self.metric.get()
        metrics = np.array(metrics)
        metrics *= 100
        print('''\
Accuracy: {0}
Accuracy Class: {1}
Mean IU: {2}
FWAV Accuracy: {3}'''.format(*metrics))
        self.metric.reset()

    def forward(self, score, target):
        self.metric.update(score, target)

    def forward_shape(self, *input_shpaes):
        return
