# --------------------------------------------------------
# PyTorchCaffe
# Licensed under The MIT License [see LICENSE for details]
# Written by zhaojianying and xiaohang 2018.03
# --------------------------------------------------------

from __future__ import division, print_function

import sys
import os
import cv2
import numpy as np
import math

import torch
import torch.nn as nn
import torch.utils.data as data

from .augmentations import SSDAugmentation, SSDEvalTransform
from ptcaffe.utils.config import cfg
from ptcaffe.layer_dict import register_data_layer
from collections import OrderedDict

if sys.version_info[0] == 2:
    import xml.etree.cElementTree as ET
else:
    import xml.etree.ElementTree as ET

def parse_yolo2_annotation(annopath, class_to_ind, width, height):
    lines = open(annopath).readlines()
    if len(lines) == 0:
        return []
    res = []
    for idx, line in enumerate(lines):
        items = line.split()
        cx = float(items[1])
        cy = float(items[2])
        w = float(items[3])
        h = float(items[4])
        x1 = cx - w / 2.0
        y1 = cy - h / 2.0
        x2 = cx + w / 2.0
        y2 = cy + h / 2.0
        label = int(items[0]) + 1
        bndbox = [x1, y1, x2, y2, label]
        res.append(bndbox)
        res.append(0) # difficult
    return res

def parse_xml_annotation(annopath, class_to_ind, width, height, keep_difficult):
    target = ET.parse(annopath).getroot()
    res = []
    for obj in target.iter('object'):
        difficult = int(obj.find('difficult').text) == 1
        if not keep_difficult and difficult:
            continue
        name = obj.find('name').text.lower().strip()
        bbox = obj.find('bndbox')

        pts = ['xmin', 'ymin', 'xmax', 'ymax']
        bndbox = []
        for i, pt in enumerate(pts):
            cur_pt = float(bbox.find(pt).text) - 1
            # scale height or width
            cur_pt = cur_pt / width if i % 2 == 0 else cur_pt / height
            bndbox.append(cur_pt)
        label_idx = class_to_ind[name] + 1 # 0 for background
        bndbox.append(label_idx)
        bndbox.append(difficult)
        res += [bndbox]  # [xmin, ymin, xmax, ymax, label_ind]

    return res

class SSDListDataset(data.Dataset):
    def __init__(self, listfile, phase, classes = ('face',), keep_difficult=True, transform=None, target_transform=None):
        self.listfile = listfile
        self.phase = phase
        self.transform = transform
        self.target_transform = target_transform
        self.lines = open(listfile).readlines()
        self.class_to_ind = dict(zip(classes, range(len(classes))))
        self.keep_difficult = keep_difficult

    def __len__(self):
        return len(self.lines)

    def __getitem__(self, index):
        index = index % len(self)
        imgpath, annopath = self.lines[index].strip().split()
        if (not os.path.exists(imgpath)) or (not os.path.exists(annopath)):
            return self[index+1]

        img = cv2.imread(imgpath)
        height, width, channels = img.shape
        if annopath.find(".xml") >= 0:
            target = parse_xml_annotation(annopath, self.class_to_ind, width, height, self.keep_difficult)
        elif annopath.find(".txt") >= 0:
            target = parse_yolo2_annotation(annopath, self.class_to_ind, width, height)
        
        if len(target) == 0:
            return self[index+1]
        
        if self.target_transform is not None:
            target = self.target_transform(target)

        if self.transform is not None:
            target = np.array(target)
            img, boxes, labels = self.transform(img, target[:, :4], target[:, 4])
            if self.phase == 'TRAIN':
                difficults = np.array([0] * len(labels))
            else:
                difficults = target[:, 5]
            target = np.hstack((boxes, np.expand_dims(labels, axis=1), np.expand_dims(difficults, axis=1)))
        return torch.from_numpy(img).permute(2, 0, 1), target

def SSD_detection_collate(batch):
    targets = []
    imgs = []
    for idx, sample in enumerate(batch):
        imgs.append(sample[0])
        bboxes = sample[1]
        for bbox in bboxes:
            targets.append([idx, bbox[4], -1, bbox[0], bbox[1], bbox[2], bbox[3], bbox[5]])
    return torch.stack(imgs, 0), torch.FloatTensor(targets).unsqueeze(0).unsqueeze(0)

@register_data_layer('SSDListData')
class SSDListData(nn.Module):
    """
    layer {
        name: "ssd_data"
        type: "SSDListData"
        top: "data"
        top: "label"
        include {
            phase: TRAIN
        }
        list_data_param {
            source: "list.txt"
            classes: "face,people"
            mirror: true
            mean_value: 104.0
            mean_value: 117.0
            mean_value: 123.0
            batch_size: 32
            num_workers: 8
            width: 512
            height: 512
            channels: 3
        }
    }
    """

    VOC_CLASSES = ('aeroplane', 'bicycle', 'bird', 'boat',
           'bottle', 'bus', 'car', 'cat', 'chair',
           'cow', 'diningtable', 'dog', 'horse',
           'motorbike', 'person', 'pottedplant',
           'sheep', 'sofa', 'train', 'tvmonitor')

    def __init__(self, layer):
        super(SSDListData, self).__init__()
        source = layer['list_data_param']['source']
        phase = layer['include']['phase'] if 'include' in layer and 'phase' in layer['include'] else 'TRAIN'
        list_data_param = layer.get('list_data_param', OrderedDict())
        if 'classes_type' in list_data_param:
            classes_type = list_data_param['classes_type']
            if classes_type == 'pascal':
                classes = SSDListData.VOC_CLASSES
            else:
                assert False
        else:
            classes = list_data_param['classes']
            classes = classes.split(',')
        mean_vals = list_data_param['mean_value']
        mean_vals = [float(val) for val in mean_vals]
      
        if 'batch_size' in list_data_param:
            batch_size = int(list_data_param['batch_size'])
        elif 'base_batch_size' in list_data_param:
            num_gpus = cfg.NUM_GPUS if cfg.NUM_GPUS is not None else 1
            batch_size = int(list_data_param['base_batch_size']) * num_gpus

        num_workers = int(list_data_param['num_workers'])
        width = int(list_data_param['width'])
        height = int(list_data_param['height'])
        assert(width == height)
        ssd_dim = width
        channels = int(list_data_param['channels'])
        expand_prob = list_data_param.get('expand_prob', 0.5)
        expand_ratio = list_data_param.get('expand_ratio', 4)
        tf_adjust = (list_data_param.get('tf_adjust', 'false') == 'true')
        keep_difficult = (list_data_param.get('keep_difficult', 'true') == 'true')
        if phase == 'TRAIN':
            dataset = SSDListDataset(source, phase, classes, keep_difficult, SSDAugmentation(ssd_dim, mean_vals, expand_prob, expand_ratio, tf_adjust))
            self.data_loader = data.DataLoader(dataset, batch_size, num_workers=num_workers, shuffle=True, collate_fn=SSD_detection_collate, pin_memory=True)
        else:
            dataset = SSDListDataset(source, phase, classes, keep_difficult, SSDEvalTransform(ssd_dim, mean_vals, tf_adjust))
            #dataset = SSDListDataset(source, classes, keep_difficult, None)
            self.data_loader = data.DataLoader(dataset, batch_size, num_workers=num_workers, shuffle=False, collate_fn=SSD_detection_collate, pin_memory=True)
        self.batch_iterator = iter(self.data_loader)
        self.batch_num = len(dataset) // batch_size
        print('self.batch_num = %d' % self.batch_num)
        self.iteration = 0

        tname = layer['top']
        self.tnames = tname if type(tname) == list else [tname]

        self.device = -1

        self.width = width
        self.height = height
        self.channels = channels
        self.batch_size = batch_size
        self.iter_id = 0

    def __repr__(self):
        return 'SSDListData()'

    def forward_shape(self):
        image_shape = [self.batch_size, self.channels, self.height, self.width]
        label_shape = [1, 1, 1, 8]
        return image_shape, label_shape

    def set_device(self, device):
        if device is None:
            self.device = 0
        else:
            self.device = device

    def forward(self):
        if self.iteration > 0 and self.iteration % self.batch_num == 0:
            self.batch_iterator = iter(self.data_loader)
            self.iteration = 0
            print('reset batch_iterator')

        fetch_datas = next(self.batch_iterator)
        if False:
            from PIL import Image, ImageDraw
            images = fetch_datas[0].numpy()
            labels = fetch_datas[1].numpy()
            targets = labels.reshape(-1, 8)
            widths = (targets[:,5] - targets[:,3])*640
            heights = (targets[:,6] - targets[:,4])*640
            areas = widths * heights
            min_area,min_id = torch.from_numpy(areas).min(0)
            print('label areas:', min_area, min_id)
            min_id = int(targets[min_id[0]][0])
            image = images[min_id]
            image[0] = image[0] + 104
            image[1] = image[1] + 117
            image[2] = image[2] + 123
            image = image.transpose(1,2,0)
            image = image[:,:,::-1]
            image = Image.fromarray(image.astype(np.uint8))
            image.save('save%d_orig.jpg' % self.iter_id)
            print('save image save%d_orig.jpg' % self.iter_id)
            draw = ImageDraw.Draw(image)
            for i in range(targets.shape[0]):
                batch_id = int(targets[i][0])
                if batch_id != min_id:
                    continue
                label = targets[i]
                x1 = label[3] * 640
                y1 = label[4] * 640
                x2 = label[5] * 640
                y2 = label[6] * 640
                area = (x2-x1)*(y2-y1)
                draw.rectangle([x1,y1, x2,y2])
                draw.text((x1,y1), "%d" % int(round(area)))
            image.save('save%d_draw.jpg' % self.iter_id)
            print('save image save%d_draw.jpg' % self.iter_id)
            self.iter_id += 1
        self.iteration += 1
        outputs = []
        for idx, name in enumerate(self.tnames):
            data = fetch_datas[idx]
            if self.device != -1:
                outputs.append(data.cuda(self.device))
            else:
                outputs.append(data)
        return tuple(outputs)
