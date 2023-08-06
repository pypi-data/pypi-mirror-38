from __future__ import division, print_function

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from collections import OrderedDict

from ptcaffe.layer_dict import register_data_layer, CaffeData

@register_data_layer('ImageSegData')
class ImageSegData(CaffeData):
    def __init__(self, layer):
        super(ImageSegData, self).__init__(layer)

    def __repr__(self):
        return "ImageSegData()"

    def get_batch_size(self):
        image_data_param = self.layer.get('image_data_param', OrderedDict())
        return int(image_data_param['batch_size'])

    def get_batch_num(self):
        image_data_param = self.layer.get('image_data_param', OrderedDict())
        source_file = image_data_param['source']
        batch_size = int(image_data_param['batch_size'])
        with open(source_file, 'r') as fp:
            lines = fp.readlines()
        return int(len(lines) / float(batch_size))
