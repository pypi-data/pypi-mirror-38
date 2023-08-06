import torch
import torch.nn as nn
from collections import OrderedDict
import copy

class Reorg(nn.Module):
    def __init__(self, layer, input_shape):
        super(Reorg, self).__init__()
        reorg_param = layer.get('reorg_param', OrderedDict())
        self.use_correct_reorg = (layer.get('use_correct_reorg', 'false') == 'true')
        stride = int(reorg_param.get('stride', 2))
        self.stride = stride

    def __repr__(self):
        return 'Reorg(stride=%d)' % self.stride

    def forward(self, x):
        stride = self.stride
        assert(x.data.dim() == 4)
        B = x.data.size(0)
        C = x.data.size(1)
        H = x.data.size(2)
        W = x.data.size(3)
        assert(H % stride == 0)
        assert(W % stride == 0)
        ws = stride
        hs = stride
        if self.use_correct_reorg:
            x = x.view(B, C, H/hs, hs, W/ws, ws).permute(0,3,5,1,2,4).contiguous().view(B,hs*ws*C, H/hs, W/ws)
        else:
            FC = C/hs/ws
            FH = H*hs
            FW = W*hs
            x = x.view(B, FC, FH/hs, hs, FW/ws, ws).permute(0,3,5,1,2,4).contiguous().view(B,hs*ws*C, H/hs, W/ws)
        return x

    def forward_shape(self, input_shape):
        B = input_shape[0]
        C = input_shape[1]
        H = input_shape[2]
        W = input_shape[3]
        output_shape = [B, C*self.stride*self.stride, int(H/self.stride), int(W/self.stride)]
        return output_shape
