# -*- coding:utf-8 -*- 
from __future__ import division, print_function

import torch
import torch.nn as nn
from ptcaffe.layer_dict import register_layer
from collections import OrderedDict, defaultdict
import numpy as np
import threading

from ptcaffe.utils.logger import logger
from .voc_detection import bbox_iou
from .detection_output_layer import DetectionOutput

@register_layer('DetectionEvaluate2')
class DetectionEvaluate2(nn.Module):
    def __init__(self, layer, *input_shapes):
        super(DetectionEvaluate2, self).__init__()
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

        from voc_detection import VOCMApMetricCaffe
        self.use_07_metric = (detection_evaluate_param.get('use_07_metric', 'false') == 'true')

        if self.use_07_metric:
            ap_version = "11point"
        else:
            ap_version = "MaxIntegral"
        self.metric = VOCMApMetricCaffe(iou_thresh=self.overlap_threshold, class_names=self.classes,
            ap_version=ap_version)

        self.lock = threading.Lock()
        self.device = -1
        self.devices = [-1]
        self.tname = layer.get('top', None)

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
        if self.tname is not None:
            return [1, 5]

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
        _n_pos, _score_list, _match_list = self.match(pred_bboxes, pred_labels, pred_scores, gt_bboxes, gt_labels, gt_difficults)
        num_preds = detection_out.shape[0]
        output = torch.zeros(self.num_classes - 1 + num_preds, 5)
        for c in range(1, self.num_classes):
            output[c-1, 0] = -1
            output[c-1, 1] = c
            output[c-1, 2] = _n_pos[c]
            output[c-1, 3] = -1
            output[c-1, 4] = -1

        idx = self.num_classes - 1
        for b in range(B):
            _score = _score_list[b]
            _match = _match_list[b]
            for c in range(1, self.num_classes):
                if c not in _score: continue
                for i,s in enumerate(_score[c]):
                    output[idx, 0] = b
                    output[idx, 1] = c
                    output[idx, 2] = float(s)
                    if _match[c][i] == -1:
                        output[idx, 3] = 0 # -1
                        output[idx, 4] = 0 #-1
                    else:
                        output[idx, 3] = _match[c][i]
                        output[idx, 4] = 1 - _match[c][i]
                    idx += 1
        self.metric.update(output.data.numpy())

        if self.tname is not None:
            return output

    def match(self, pred_bboxes, pred_labels, pred_scores, gt_bboxes, gt_labels, gt_difficults):
        def as_numpy(a):
            """Convert a (list of) numpy.ndarray into numpy.ndarray"""
            if isinstance(a, (list, tuple)):
                out = [np.array(x) if isinstance(x, (list, tuple)) else x for x in a]
                out = np.array(out)
                return np.concatenate(out, axis=0)
            elif isinstance(a, np.ndarray):
                a = np.array(a)
            return a

        if gt_difficults is None:
            gt_difficults = [None for _ in gt_labels]

        _n_pos = defaultdict(int)
        _score_list = []
        _match_list = []
        image_id = -1
        for pred_bbox, pred_label, pred_score, gt_bbox, gt_label, gt_difficult in zip(
                *[as_numpy(x) for x in [pred_bboxes, pred_labels, pred_scores,
                                        gt_bboxes, gt_labels, gt_difficults]]):
            image_id += 1
            _score = defaultdict(list)
            _match = defaultdict(list)
            _score_list.append(_score)
            _match_list.append(_match)

            # strip padding -1 for pred and gt
            valid_pred = np.where(pred_label.flat >= 0)[0]
            pred_bbox = pred_bbox[valid_pred, :]
            pred_label = pred_label.flat[valid_pred].astype(int)
            pred_score = pred_score.flat[valid_pred]
            valid_gt = np.where(gt_label.flat >= 0)[0]
            gt_bbox = gt_bbox[valid_gt, :]
            gt_label = gt_label.flat[valid_gt].astype(int)
            if gt_difficult is None:
                gt_difficult = np.zeros(gt_bbox.shape[0])
            else:
                gt_difficult = gt_difficult.flat[valid_gt]

            for l in np.unique(np.concatenate((pred_label, gt_label)).astype(int)):
                pred_mask_l = pred_label == l
                pred_bbox_l = pred_bbox[pred_mask_l]
                pred_score_l = pred_score[pred_mask_l]
                # sort by score
                order = pred_score_l.argsort()[::-1]
                pred_bbox_l = pred_bbox_l[order]
                pred_score_l = pred_score_l[order]

                gt_mask_l = gt_label == l
                gt_bbox_l = gt_bbox[gt_mask_l]
                gt_difficult_l = gt_difficult[gt_mask_l]

                _n_pos[l] += np.logical_not(gt_difficult_l).sum()
                _score[l].extend(pred_score_l)

                if len(pred_bbox_l) == 0:
                    continue
                if len(gt_bbox_l) == 0:
                    _match[l].extend((0,) * pred_bbox_l.shape[0])
                    continue

                # VOC evaluation follows integer typed bounding boxes.
                #pred_bbox_l = pred_bbox_l.copy()
                #pred_bbox_l[:, 2:] += 1
                #gt_bbox_l = gt_bbox_l.copy()
                #gt_bbox_l[:, 2:] += 1

                iou = bbox_iou(pred_bbox_l, gt_bbox_l)
                gt_index = iou.argmax(axis=1)
                # set -1 if there is no matching ground truth
                gt_index[iou.max(axis=1) < self.overlap_threshold] = -1
                del iou

                selec = np.zeros(gt_bbox_l.shape[0], dtype=bool)
                for gt_idx in gt_index:
                    if gt_idx >= 0:
                        if gt_difficult_l[gt_idx]:
                            #import pdb; pdb.set_trace()
                            _match[l].append(-1)
                        else:
                            if not selec[gt_idx]:
                                _match[l].append(1)
                                #if image_id == 4:
                                #    pred_idx = len(_match[l])-1
                                #    tmp_score = _score[l][pred_idx]
                                #    tmp_iou = iou[pred_idx, gt_idx]
                                #    print("===== score %f matched to gt %d with iou %f" % (tmp_score, gt_idx, tmp_iou))
                            else:
                                _match[l].append(0)
                        selec[gt_idx] = True
                    else:
                        _match[l].append(0)

        return _n_pos, _score_list, _match_list

    def __repr__(self):
        return "DetectionEvaluate2()"
