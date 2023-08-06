"""Pascal VOC Detection evaluation."""
from __future__ import division, print_function

from collections import defaultdict
from ptcaffe.utils.logger import logger
import numpy as np

REC_POINTS = [0. , 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.]

def bbox_iou(bbox_a, bbox_b, offset=0):
    """Calculate Intersection-Over-Union(IOU) of two bounding boxes.
    Parameters
    ----------
    bbox_a : numpy.ndarray
        An ndarray with shape :math:`(N, 4)`.
    bbox_b : numpy.ndarray
        An ndarray with shape :math:`(M, 4)`.
    offset : float or int, default is 0
        The ``offset`` is used to control the whether the width(or height) is computed as
        (right - left + ``offset``).
        Note that the offset must be 0 for normalized bboxes, whose ranges are in ``[0, 1]``.
    Returns
    -------
    numpy.ndarray
        An ndarray with shape :math:`(N, M)` indicates IOU between each pairs of
        bounding boxes in `bbox_a` and `bbox_b`.
    """
    if bbox_a.shape[1] < 4 or bbox_b.shape[1] < 4:
        raise IndexError("Bounding boxes axis 1 must have at least length 4")

    tl = np.maximum(bbox_a[:, None, :2], bbox_b[:, :2])
    br = np.minimum(bbox_a[:, None, 2:4], bbox_b[:, 2:4])

    area_i = np.prod(br - tl + offset, axis=2) * (tl < br).all(axis=2)
    area_a = np.prod(bbox_a[:, 2:4] - bbox_a[:, :2] + offset, axis=1)
    area_b = np.prod(bbox_b[:, 2:4] - bbox_b[:, :2] + offset, axis=1)
    return area_i / (area_a[:, None] + area_b - area_i)

def cumsum(pairs):
    pair_scores = np.array([p[0] for p in pairs])
    order = np.argsort(pair_scores)[::-1]
    for i, o in enumerate(order):
        if (i == 0):
            cumsum = [pairs[o][1]]
        else:
            cumsum.append(pairs[o][1] + cumsum[-1])
    return cumsum


class EvalMetric(object):
    """Base class for all evaluation metrics.

    .. note::

        This is a base class that provides common metric interfaces.
        One should not use this class directly, but instead create new metric
        classes that extend it.

    Parameters
    ----------
    name : str
        Name of this metric instance for display.
    output_names : list of str, or None
        Name of predictions that should be used when updating with update_dict.
        By default include all predictions.
    label_names : list of str, or None
        Name of labels that should be used when updating with update_dict.
        By default include all labels.
    """
    def __init__(self, name, output_names=None,
                 label_names=None, **kwargs):
        self.name = str(name)
        self.output_names = output_names
        self.label_names = label_names
        self._kwargs = kwargs
        self.reset()

    def __str__(self):
        return "EvalMetric: {}".format(dict(self.get_name_value()))

    def get_config(self):
        """Save configurations of metric. Can be recreated
        from configs with metric.create(**config)
        """
        config = self._kwargs.copy()
        config.update({
            'metric': self.__class__.__name__,
            'name': self.name,
            'output_names': self.output_names,
            'label_names': self.label_names})
        return config

    def update_dict(self, label, pred):
        """Update the internal evaluation with named label and pred

        Parameters
        ----------
        labels : OrderedDict of str -> NDArray
            name to array mapping for labels.

        preds : OrderedDict of str -> NDArray
            name to array mapping of predicted outputs.
        """
        if self.output_names is not None:
            pred = [pred[name] for name in self.output_names]
        else:
            pred = list(pred.values())

        if self.label_names is not None:
            label = [label[name] for name in self.label_names]
        else:
            label = list(label.values())

        self.update(label, pred)

    def update(self, labels, preds):
        """Updates the internal evaluation result.

        Parameters
        ----------
        labels : list of `NDArray`
            The labels of the data.

        preds : list of `NDArray`
            Predicted values.
        """
        raise NotImplementedError()

    def reset(self):
        """Resets the internal evaluation result to initial state."""
        self.num_inst = 0
        self.sum_metric = 0.0

    def get(self):
        """Gets the current evaluation result.

        Returns
        -------
        names : list of str
           Name of the metrics.
        values : list of float
           Value of the evaluations.
        """
        if self.num_inst == 0:
            return (self.name, float('nan'))
        else:
            return (self.name, self.sum_metric / self.num_inst)

    def get_name_value(self):
        """Returns zipped name and value pairs.

        Returns
        -------
        list of tuples
            A (name, value) tuple list.
        """
        name, value = self.get()
        if not isinstance(name, list):
            name = [name]
        if not isinstance(value, list):
            value = [value]
        return list(zip(name, value))

class VOCMApMetric(EvalMetric):
    """
    Calculate mean AP for object detection task
    Parameters:
    ---------
    iou_thresh : float
        IOU overlap threshold for TP
    class_names : list of str
        optional, if provided, will print out AP for each class
    """
    def __init__(self, iou_thresh=0.5, class_names=None):
        super(VOCMApMetric, self).__init__('VOCMeanAP')
        if class_names is None:
            self.num = None
        else:
            assert isinstance(class_names, (list, tuple))
            for name in class_names:
                assert isinstance(name, str), "must provide names as str"
            num = len(class_names)
            self.name = list(class_names) + ['mAP']
            self.num = num + 1
        self.reset()
        self.iou_thresh = iou_thresh
        self.class_names = class_names

    def reset(self):
        """Clear the internal statistics to initial state."""
        if getattr(self, 'num', None) is None:
            self.num_inst = 0
            self.sum_metric = 0.0
        else:
            self.num_inst = [0] * self.num
            self.sum_metric = [0.0] * self.num
        self._n_pos = defaultdict(int)
        self._score = defaultdict(list)
        self._match = defaultdict(list)

    def get(self):
        """Get the current evaluation result.
        Returns
        -------
        name : str
           Name of the metric.
        value : float
           Value of the evaluation.
        """
        self._update()  # update metric at this time
        if self.num is None:
            if self.num_inst == 0:
                return (self.name, float('nan'))
            else:
                return (self.name, self.sum_metric / self.num_inst)
        else:
            names = ['%s'%(self.name[i]) for i in range(self.num)]
            values = [x / y if y != 0 else float('nan') \
                for x, y in zip(self.sum_metric, self.num_inst)]
            return (names, values)

    # pylint: disable=arguments-differ, too-many-nested-blocks
    def update(self, pred_bboxes, pred_labels, pred_scores,
               gt_bboxes, gt_labels, gt_difficults=None):
        """Update internal buffer with latest prediction and gt pairs.
        Parameters
        ----------
        pred_bboxes : numpy.ndarray
            Prediction bounding boxes with shape `B, N, 4`.
            Where B is the size of mini-batch, N is the number of bboxes.
        pred_labels : numpy.ndarray
            Prediction bounding boxes labels with shape `B, N`.
        pred_scores : numpy.ndarray
            Prediction bounding boxes scores with shape `B, N`.
        gt_bboxes : numpy.ndarray
            Ground-truth bounding boxes with shape `B, M, 4`.
            Where B is the size of mini-batch, M is the number of ground-truths.
        gt_labels : numpy.ndarray
            Ground-truth bounding boxes labels with shape `B, M`.
        gt_difficults : numpy.ndarray, optional, default is None
            Ground-truth bounding boxes difficulty labels with shape `B, M`.
        """
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

        for pred_bbox, pred_label, pred_score, gt_bbox, gt_label, gt_difficult in zip(
                *[as_numpy(x) for x in [pred_bboxes, pred_labels, pred_scores,
                                        gt_bboxes, gt_labels, gt_difficults]]):
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

                self._n_pos[l] += np.logical_not(gt_difficult_l).sum()
                self._score[l].extend(pred_score_l)

                if len(pred_bbox_l) == 0:
                    continue
                if len(gt_bbox_l) == 0:
                    self._match[l].extend((0,) * pred_bbox_l.shape[0])
                    continue

                # VOC evaluation follows integer typed bounding boxes.
                #pred_bbox_l = pred_bbox_l.copy()
                #pred_bbox_l[:, 2:] += 1
                #gt_bbox_l = gt_bbox_l.copy()
                #gt_bbox_l[:, 2:] += 1

                iou = bbox_iou(pred_bbox_l, gt_bbox_l)
                gt_index = iou.argmax(axis=1)
                # set -1 if there is no matching ground truth
                gt_index[iou.max(axis=1) < self.iou_thresh] = -1
                del iou

                selec = np.zeros(gt_bbox_l.shape[0], dtype=bool)
                for gt_idx in gt_index:
                    if gt_idx >= 0:
                        if gt_difficult_l[gt_idx]:
                            self._match[l].append(-1)
                        else:
                            if not selec[gt_idx]:
                                self._match[l].append(1)
                            else:
                                self._match[l].append(0)
                        selec[gt_idx] = True
                    else:
                        self._match[l].append(0)

        #  aps = []
        #  recall, precs = self._recall_prec()
        #  for l, rec, prec in zip(range(len(precs)), recall, precs):
            #  ap = self._average_precision(rec, prec)
            #  aps.append(ap)
            #  if self.num is not None and l < (self.num - 1):
                #  self.sum_metric[l] = ap
                #  self.num_inst[l] = 1
        #  if self.num is None:
            #  self.num_inst = 1
            #  self.sum_metric = np.nanmean(aps)
        #  else:
            #  self.num_inst[-1] = 1
            #  self.sum_metric[-1] = np.nanmean(aps)

    def _update(self):
        """ update num_inst and sum_metric """
        aps = []
        recall, precs = self._recall_prec()
        for l, rec, prec in zip(range(len(precs)), recall, precs):
            ap = self._average_precision(rec, prec)
            aps.append(ap)
            if self.num is not None and l < (self.num - 1):
                self.sum_metric[l] = ap
                self.num_inst[l] = 1
        if self.num is None:
            self.num_inst = 1
            self.sum_metric = np.nanmean(aps)
        else:
            self.num_inst[-1] = 1
            self.sum_metric[-1] = np.nanmean(aps)

    def _recall_prec(self):
        """ get recall and precision from internal records """
        n_fg_class = max(self._n_pos.keys()) + 1
        prec = [None] * n_fg_class
        rec = [None] * n_fg_class

        for l in self._n_pos.keys():
            score_l = np.array(self._score[l])
            match_l = np.array(self._match[l], dtype=np.int32)

            order = score_l.argsort()[::-1]
            match_l = match_l[order]

            tp = np.cumsum(match_l == 1)
            fp = np.cumsum(match_l == 0)

            # If an element of fp + tp is 0,
            # the corresponding element of prec[l] is nan.
            with np.errstate(divide='ignore', invalid='ignore'):
                prec[l] = tp / (fp + tp)
            # If n_pos[l] is 0, rec[l] is None.
            if self._n_pos[l] > 0:
                rec[l] = tp / self._n_pos[l]

        return rec, prec

    def _average_precision(self, rec, prec):
        """
        calculate average precision
        Params:
        ----------
        rec : numpy.array
            cumulated recall
        prec : numpy.array
            cumulated precision
        Returns:
        ----------
        ap as float
        """
        if rec is None or prec is None:
            return np.nan

        # append sentinel values at both ends
        mrec = np.concatenate(([0.], rec, [1.]))
        mpre = np.concatenate(([0.], np.nan_to_num(prec), [0.]))

        # compute precision integration ladder
        for i in range(mpre.size - 1, 0, -1):
            mpre[i - 1] = np.maximum(mpre[i - 1], mpre[i])

        # look for recall value changes
        i = np.where(mrec[1:] != mrec[:-1])[0]

        # sum (\delta recall) * prec
        ap = np.sum((mrec[i + 1] - mrec[i]) * mpre[i + 1])
        return ap


class VOC07MApMetric(VOCMApMetric):
    """ Mean average precision metric for PASCAL V0C 07 dataset
    Parameters:
    ---------
    iou_thresh : float
        IOU overlap threshold for TP
    class_names : list of str
        optional, if provided, will print out AP for each class
    """
    def __init__(self, *args, **kwargs):
        super(VOC07MApMetric, self).__init__(*args, **kwargs)

    def _average_precision(self, rec, prec):
        """
        calculate average precision, override the default one,
        special 11-point metric
        Params:
        ----------
        rec : numpy.array
            cumulated recall
        prec : numpy.array
            cumulated precision
        Returns:
        ----------
        ap as float
        """
        if rec is None or prec is None:
            return np.nan
        ap = 0.
        for t in REC_POINTS:
            if np.sum(rec >= t) == 0:
                p = 0
            else:
                p = np.max(np.nan_to_num(prec)[rec >= t])
            ap += p / 11.
        return ap

class VOCMApMetricCaffe(EvalMetric):
    """ Mean average precision metric for PASCAL V0C dataset
    Parameters:
    ---------
    iou_thresh : float
        IOU overlap threshold for TP
    class_names : list of str
        optional, if provided, will print out AP for each class
    ap_version : str
        one of 11point MaxIntegral Integral
    """
    def __init__(self, iou_thresh=0.5, class_names=None, ap_version='11point'):
        super(VOCMApMetricCaffe, self).__init__('VOCMeanAP')
        if class_names is None:
            self.num = None
        else:
            assert isinstance(class_names, (list, tuple))
            for name in class_names:
                assert isinstance(name, str), "must provide names as str"
            num = len(class_names)
            self.name = list(class_names) + ['mAP']
            self.num = num + 1
        self.reset()
        self.iou_thresh = iou_thresh
        self.class_names = class_names
        self.ap_version = ap_version

    def reset(self):
        """Clear the internal statistics to initial state."""
        if getattr(self, 'num', None) is None:
            self.num_inst = 0
            self.sum_metric = 0.0
        else:
            self.num_inst = [0] * self.num
            self.sum_metric = [0.0] * self.num
        self.all_num_pos = defaultdict(int)
        self.all_true_pos = defaultdict(list)
        self.all_false_pos = defaultdict(list)

    def update(self, result):
        assert(result.shape[1] == 5)
        num_det = result.shape[0]
        #print("num_det: {}".format(num_det))
        for k in range(num_det):
            item_id = int(result[k, 0])
            label = int(result[k, 1])
            #  if int(label) == 6 and item_id is not -1:
                #  import pdb; pdb.set_trace()
            if item_id == -1: # Special row of storing number of positives for a label
                if not self.all_num_pos.has_key(label):
                    self.all_num_pos[label] = int(result[k, 2])
                else:
                    self.all_num_pos[label] += int(result[k, 2])
            else: # Normal row storing detection status.
                score = result[k, 2]
                tp = int(result[k, 3])
                fp = int(result[k, 4])
                #print("label: {} score: {} tp: {} fp: {}".format(label, score, tp, fp))
                if tp == 0 and fp == 0:
                    continue
                self.all_true_pos[label].append((score, tp))
                self.all_false_pos[label].append((score, fp))

    def get(self,):
        assert self.all_true_pos.keys() is not [], "Missing output_blob true_pos"
        assert self.all_false_pos.keys() is not [], "Missing output_blob false_pos"
        assert self.all_num_pos.keys() is not [], "Missing output_blob num_pos"
        APs = defaultdict()
        mAP = 0.0
        for label in self.all_num_pos.keys():
            label_num_pos = self.all_num_pos[label]
            if not self.all_true_pos.has_key(label):
                logger.warning("Missing true_pos for label: {}".format(label))
                continue
            label_true_pos = self.all_true_pos[label]
            if not self.all_false_pos.has_key(label):
                logger.warning("Missing false_pos for label: {}".format(label))
                continue
            label_false_pos = self.all_false_pos[label]

            #print("class{} num_tp: {}".format(int(label), len(label_true_pos)))

            #  if label == 7:
                #  import pdb; pdb.set_trace()

            prec, rec, APs[label] = self._average_precision(label_true_pos, label_num_pos, label_false_pos,
                self.ap_version)

            #print("class{} prec: {}".format(int(label), prec))
            #print("class{} rec: {}".format(int(label), rec))
            mAP += APs[label]
        mAP /= len(self.all_num_pos.keys())

        if self.num is None:
            return (self.name, mAP)
        else:
            values = APs
            values[self.num - 1] = mAP
            names = ['%s'%(self.name[int(i)]) for i in values.keys()]
            #names = ['class%s'%(int(i)) for i in values.keys()]
            return (names, values.values())



    def _average_precision(self, tp, num_pos, fp, ap_version):
        eps = 1e-6
        assert len(tp) == len(fp), "tp must have same size as fp."
        num = len(tp)

        for i in range(num):
            assert abs(tp[i][0] - fp[i][0]) <= eps
            #assert tp[i][1] == 1 - fp[i][1]

        prec = []
        rec = []
        ap = 0.

        if len(tp) == 0 or num_pos == 0:
            return [], [], ap

        tp_cumsum = cumsum(tp)
        fp_cumsum = cumsum(fp)
        assert len(tp_cumsum) == num
        assert len(fp_cumsum) == num

        for i in range(num):
            prec.append(float(tp_cumsum[i]) / (tp_cumsum[i] + fp_cumsum[i]))
            assert tp_cumsum[i] <= num_pos
            rec.append(float(tp_cumsum[i]) / num_pos)

        if ap_version is "11point":
            max_precs = np.zeros((11))
            start_idx = num - 1
            for j in range(10, -1, -1):
                for i in range(start_idx, -1, -1):
                    if rec[i] < REC_POINTS[j]:
                        start_idx = i
                        if j > 0:
                            max_precs[j-1] = max_precs[j]
                        if logger.getEffectiveLevel() >= logger.DEBUG:
                            logger.debug("j: {} i: {} reci: {} j/10: {}".format(j, i, rec[i], j/10.))
                        break
                    else:
                      if max_precs[j] < prec[i]:
                          max_precs[j] = prec[i]
            for max_prec in max_precs:
                ap += max_prec / 11.0
        elif ap_version is "MaxIntegral":
            cur_rec = rec[-1]
            cur_prec = prec[-1]
            for i in range(num - 2, -1, -1):
                cur_prec = max(prec[i], cur_prec)
                if abs(cur_rec - rec[i]) > eps:
                    ap += cur_prec * abs(cur_rec - rec[i])
                cur_rec = rec[i]
            ap += cur_rec * cur_prec
        elif ap_version is "Integral":
            prev_rec = 0.
            for i in range(num):
                if abs(rec[i] - prev_rec) > eps:
                    ap += prec[i] * abs(rec[i] - prev_rec)
                prev_rec = rec[i]
        else:
          logger.error("Unknown ap_version: {}".format(ap_version))
          exit()

        return prec, rec, ap
