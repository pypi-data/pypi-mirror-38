import torch
import torch.nn as nn
from collections import OrderedDict
import copy

class YoloUpsample(nn.Module):
    def __init__(self, layer, input_shape):
        super(YoloUpsample, self).__init__()
        upsample_param = layer.get('upsample_param', OrderedDict())
        self.stride = int(upsample_param['stride'])

    def __repr__(self):
        return "YoloUpsample()"

    def forward(self, x):
        stride = self.stride
        assert(x.data.dim() == 4)
        B = x.data.size(0)
        C = x.data.size(1)
        H = x.data.size(2)
        W = x.data.size(3)
        ws = stride
        hs = stride
        x = x.view(B, C, H, 1, W, 1).expand(B, C, H, stride, W, stride).contiguous().view(B, C, H*stride, W*stride)
        return x

    def forward_shape(self, input_shape):
        output_shape = copy.copy(input_shape)
        output_shape[2] = input_shape[2] * self.stride
        output_shape[3] = input_shape[3] * self.stride
        return output_shape


