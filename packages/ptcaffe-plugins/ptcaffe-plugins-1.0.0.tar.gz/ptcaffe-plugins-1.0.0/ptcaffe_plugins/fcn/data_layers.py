#!/usr/bin/env python

from __future__ import division, print_function

import math
import collections
import os.path as osp

import numpy as np
import PIL.Image
import scipy.io
import torch
import torch.nn as nn
from torch.utils import data

from ptcaffe.layers import BaseData
from ptcaffe.layer_dict import register_data_layer
from ptcaffe.utils.utils import get_visdom
from ptcaffe.utils.config import cfg


# from https://github.com/wkentaro/pytorch-fcn
class VOCClassSegBase(data.Dataset):

    class_names = np.array([
        'background',
        'aeroplane',
        'bicycle',
        'bird',
        'boat',
        'bottle',
        'bus',
        'car',
        'cat',
        'chair',
        'cow',
        'diningtable',
        'dog',
        'horse',
        'motorbike',
        'person',
        'potted plant',
        'sheep',
        'sofa',
        'train',
        'tv/monitor',
    ])
    mean_bgr = np.array([104.00698793, 116.66876762, 122.67891434])

    def __init__(self, root, split='train', transform=False):
        self.root = root
        self.split = split
        self._transform = transform

        # VOC2011 and others are subset of VOC2012
        dataset_dir = osp.join(self.root, 'VOCdevkit/VOC2012')
        self.files = collections.defaultdict(list)
        for split in ['train', 'val']:
            imgsets_file = osp.join(
                dataset_dir, 'ImageSets/Segmentation/%s.txt' % split)
            for did in open(imgsets_file):
                did = did.strip()
                img_file = osp.join(dataset_dir, 'JPEGImages/%s.jpg' % did)
                lbl_file = osp.join(
                    dataset_dir, 'SegmentationClass/%s.png' % did)
                self.files[split].append({
                    'img': img_file,
                    'lbl': lbl_file,
                })

    def __len__(self):
        return len(self.files[self.split])

    def __getitem__(self, index):
        data_file = self.files[self.split][index]
        # load image
        img_file = data_file['img']
        img = PIL.Image.open(img_file)
        img = np.array(img, dtype=np.uint8)
        # load label
        lbl_file = data_file['lbl']
        lbl = PIL.Image.open(lbl_file)
        lbl = np.array(lbl, dtype=np.int32)
        lbl[lbl == 255] = -1
        if self._transform:
            return self.transform(img, lbl)
        else:
            return img, lbl

    def transform(self, img, lbl):
        img = img[:, :, ::-1]  # RGB -> BGR
        img = img.astype(np.float64)
        img -= self.mean_bgr
        img = img.transpose(2, 0, 1)
        img = torch.from_numpy(img).float()
        lbl = torch.from_numpy(lbl).long()
        return img, lbl

    def untransform(self, img, lbl):
        img = img.numpy()
        img = img.transpose(1, 2, 0)
        img += self.mean_bgr
        img = img.astype(np.uint8)
        img = img[:, :, ::-1]
        lbl = lbl.numpy()
        return img, lbl


class VOC2011ClassSeg(VOCClassSegBase):

    def __init__(self, root, imagesets_file, split='train', transform=False):
        super(VOC2011ClassSeg, self).__init__(
            root, split=split, transform=transform)
        dataset_dir = osp.join(self.root, 'VOCdevkit/VOC2012')
        for did in open(imagesets_file):
            did = did.strip()
            img_file = osp.join(dataset_dir, 'JPEGImages/%s.jpg' % did)
            lbl_file = osp.join(dataset_dir, 'SegmentationClass/%s.png' % did)
            self.files['seg11valid'].append({'img': img_file, 'lbl': lbl_file})


class VOC2012ClassSeg(VOCClassSegBase):

    url = 'http://host.robots.ox.ac.uk/pascal/VOC/voc2012/VOCtrainval_11-May-2012.tar'  # NOQA

    def __init__(self, root, split='train', transform=False):
        super(VOC2012ClassSeg, self).__init__(
            root, split=split, transform=transform)


class SBDClassSeg(VOCClassSegBase):

    # XXX: It must be renamed to benchmark.tar to be extracted.
    url = 'http://www.eecs.berkeley.edu/Research/Projects/CS/vision/grouping/semantic_contours/benchmark.tgz'  # NOQA

    def __init__(self, root, split='train', transform=False):
        self.root = root
        self.split = split
        self._transform = transform

        dataset_dir = osp.join(self.root, 'benchmark_RELEASE/dataset')
        self.files = collections.defaultdict(list)
        for split in ['train', 'val']:
            imgsets_file = osp.join(dataset_dir, '%s.txt' % split)
            for did in open(imgsets_file):
                did = did.strip()
                img_file = osp.join(dataset_dir, 'img/%s.jpg' % did)
                lbl_file = osp.join(dataset_dir, 'cls/%s.mat' % did)
                self.files[split].append({
                    'img': img_file,
                    'lbl': lbl_file,
                })

    def __getitem__(self, index):
        data_file = self.files[self.split][index]
        # load image
        img_file = data_file['img']
        img = PIL.Image.open(img_file)
        img = np.array(img, dtype=np.uint8)
        # load label
        lbl_file = data_file['lbl']
        mat = scipy.io.loadmat(lbl_file)
        lbl = mat['GTcls'][0]['Segmentation'][0].astype(np.int32)
        lbl[lbl == 255] = -1
        if self._transform:
            return self.transform(img, lbl)
        else:
            return img, lbl


@register_data_layer('SBDClassSegData')
class SBDClassSegData(BaseData):
    def __init__(self, layer):
        super(SBDClassSegData, self).__init__(layer)
        self.visdom = None
        if 'visdom_param' in layer:
            visdom_param = layer['visdom_param']
            self.visdom = get_visdom(visdom_param, cfg)
            self.visdom_interval = int(visdom_param['interval'])
            self.title = visdom_param['title']
            self.caption = visdom_param['caption']
            self.wins = [None]

    def __repr__(self):
        return 'SBDClassSegData()'

    def create_data_loader(self, layer):
        import os.path as osp

        phase = layer['include']['phase']
        assert(phase == 'TRAIN')
        data_param = layer['data_param']
        root = data_param['data_dir'] # osp.expanduser('~/data/datasets')
        num_workers = int(data_param.get('num_workers', 4))
        kwargs = {'num_workers': num_workers, 'pin_memory': True}
        train_loader = torch.utils.data.DataLoader(
            SBDClassSeg(root, split='train', transform=True),
            batch_size=1, shuffle=True, **kwargs)
        return train_loader

    def forward(self):
        imgs, lbls = super(SBDClassSegData, self).forward()
        if self.visdom and self.batch_idx % self.visdom_interval == 0:
            win = self.wins[0]
            nrow = int(math.ceil(math.sqrt(imgs.size(0))))
            caption = "%s_batch%d" % (self.caption, self.batch_idx)
            mean_bgr = torch.FloatTensor([104.00698793, 116.66876762, 122.67891434]).view(1,3,1,1)
            disp_imgs = (imgs.cpu() + mean_bgr).numpy()
            disp_imgs = disp_imgs[:,::-1,:,:] # bgr -> rgb

            lbls_r = torch.zeros(lbls.shape)
            lbls_g = torch.zeros(lbls.shape)
            lbls_b = torch.zeros(lbls.shape)
            for i in range(1,21):
                lbls_r[lbls == i] = 0.5 # ((i+1) * 73) % 256
                lbls_g[lbls == i] = 0.5 # ((i+1) * 73 * 73) % 256
                lbls_b[lbls == i] = 0.5 # ((i+1) * 73 * 73 * 73) % 256
            disp_lbls = torch.cat([lbls_r, lbls_g, lbls_b], dim=0).unsqueeze(0)
            disp_lbls = disp_lbls.numpy()

            disp_imgs = disp_imgs * disp_lbls
  
            if win is None:
                self.wins[0] = self.visdom.images(disp_imgs, nrow=nrow, opts=dict(title=self.title, caption=caption))
                #self.wins[0] = self.visdom.images(disp_lbls, nrow=nrow, opts=dict(title=self.title, caption=caption))
            else:
                self.visdom.images(disp_imgs, nrow=nrow, opts=dict(title=self.title, caption=caption), win=win)
                #self.visdom.images(disp_lbls, nrow=nrow, opts=dict(title=self.title, caption=caption), win=win)
        return imgs, lbls

@register_data_layer('VOC2011ClassSegData')
class VOC2011ClassSegData(BaseData):
    def __init__(self, layer):
        super(VOC2011ClassSegData, self).__init__(layer)

    def __repr__(self):
        return 'VOC2011ClassSegData()'

    def create_data_loader(self, layer):
        import os.path as osp

        phase = layer['include']['phase']
        assert(phase == 'TEST')
        data_param = layer['data_param']
        root = data_param['data_dir'] #osp.expanduser('~/data/datasets')
        num_workers = int(data_param.get('num_workers'), 4)
        imagesets_file = data_param.get('imagesets', "seg11valid.txt")
        kwargs = {'num_workers': 4, 'pin_memory': True}
        val_loader = torch.utils.data.DataLoader(
            VOC2011ClassSeg(
                root, imagesets_file, split='seg11valid', transform=True),
            batch_size=1, shuffle=False, **kwargs)
        return val_loader

