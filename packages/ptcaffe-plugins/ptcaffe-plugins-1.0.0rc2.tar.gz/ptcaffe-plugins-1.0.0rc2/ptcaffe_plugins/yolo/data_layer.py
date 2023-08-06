#!/usr/bin/python
# encoding: utf-8

import os
import random
import torch
import numpy as np
from torch.utils.data import Dataset
from PIL import Image
from .utils import read_truths_args, read_truths
from .image import *

from ptcaffe.layer_dict import BaseData
from collections import OrderedDict
import torchvision

class listDataset(Dataset):

    def __init__(self, root, shape=None, shuffle=True, transform=None, target_transform=None, train=False, seen=0, batch_size=64, num_workers=4, max_boxes = 50):
       with open(root, 'r') as file:
           self.lines = file.readlines()

       if shuffle:
           random.shuffle(self.lines)

       self.nSamples  = len(self.lines)
       self.transform = transform
       self.target_transform = target_transform
       self.train = train
       self.shape = shape
       self.seen = seen
       self.batch_size = batch_size
       self.num_workers = num_workers
       self.max_boxes = max_boxes

    def __len__(self):
        return self.nSamples

    def __getitem__(self, index):
        assert index <= len(self), 'index range error'
        imgpath = self.lines[index].rstrip()

        if self.train and index % 64== 0:
            width = (random.randint(0,9) + 10)*32
            self.shape = (width, width)

        if self.train:
            jitter = 0.2
            hue = 0.1
            saturation = 1.5 
            exposure = 1.5

            img, label = load_data_detection(imgpath, self.shape, jitter, hue, saturation, exposure, max_boxes=self.max_boxes)
            label = torch.from_numpy(label)
        else:
            img = Image.open(imgpath).convert('RGB')
            if self.shape:
                img = img.resize(self.shape)
    
            labpath = imgpath.replace('images', 'labels').replace('JPEGImages', 'labels').replace('.jpg', '.txt').replace('.png','.txt')
            label = torch.zeros(self.max_boxes*5)
            #if os.path.getsize(labpath):
            #tmp = torch.from_numpy(np.loadtxt(labpath))
            try:
                tmp = torch.from_numpy(read_truths_args(labpath, 8.0/img.width).astype('float32'))
            except Exception:
                tmp = torch.zeros(1,5)
            #tmp = torch.from_numpy(read_truths(labpath))
            tmp = tmp.view(-1)
            tsz = tmp.numel()
            #print('labpath = %s , tsz = %d' % (labpath, tsz))
            if tsz > self.max_boxes*5:
                label = tmp[0:self.max_boxes*5]
            elif tsz > 0:
                label[0:tsz] = tmp

        if self.transform is not None:
            img = self.transform(img)

        if self.target_transform is not None:
            label = self.target_transform(label)

        self.seen = self.seen + self.num_workers
        return (img, label)


class Yolo2ListData(BaseData):
    def __init__(self, layer):
        super(Yolo2ListData, self).__init__(layer)

    def __repr__(self):
        return 'Yolo2ListData()'

    def create_data_loader(self, layer):
        list_param = layer.get('list_param', OrderedDict())
        
        source = list_param.get('source', '')
        assert(source != '')
        init_width = int(list_param.get('image_width', 256))
        init_height = int(list_param.get('image_height', 256))
        num_workers = int(list_param.get('num_workers', 4))
        batch_size = int(list_param.get('batch_size', 4))
        max_boxes = int(list_param.get('max_boxes', 50))
        self.device = -1
        kwargs = {'num_workers': num_workers, 'pin_memory': True}
        phase = 'TRAIN'
        if 'include' in layer and 'phase' in layer['include']:
            phase = layer['include']['phase']
        dataset = listDataset(
                        source, shape=(init_width, init_height), 
                        shuffle=(phase=='TRAIN'), 
                        transform=torchvision.transforms.Compose([torchvision.transforms.ToTensor(),]),
                        train=(phase=='TRAIN'),
                        seen=0,
                        batch_size=batch_size,
                        num_workers=num_workers,
                        max_boxes=max_boxes,
                    )
        data_loader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=False, **kwargs)
        return data_loader
