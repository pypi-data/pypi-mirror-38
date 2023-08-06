from __future__ import division, print_function

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from collections import OrderedDict

from ptcaffe.layer_dict import register_layer

@register_layer('Interp')
class Interp(nn.Module):
    def __init__(self, layer, input_shape):
        super(Interp, self).__init__()
        interp_param = layer.get('interp_param', OrderedDict())
        self.pad_beg = int(interp_param.get('pad_beg', 0))
        self.pad_end = int(interp_param.get('pad_end', 0))
        self.shrink_factor = int(interp_param['shrink_factor']) if 'shrink_factor' in interp_param else None
        self.zoom_factor = int(interp_param['zoom_factor']) if 'zoom_factor' in interp_param else None
        self.height = int(interp_param['height']) if 'height' in interp_param else None
        self.width = int(interp_param['width']) if 'width' in interp_param else None

        output_shape = self.forward_shape(input_shape)
        self.height_out = output_shape[2]
        self.width_out = output_shape[3]

    def forward_shape(self, input_shape):
        height_in = input_shape[2]
        width_in = input_shape[3] 

        height_in_eff = height_in + self.pad_beg + self.pad_end
        width_in_eff = width_in + self.pad_beg + self.pad_end

        if self.shrink_factor is not None and self.zoom_factor is None:
            height_out = int((height_in_eff - 1) / self.shrink_factor + 1)
            width_out = int((width_in_eff - 1) / self.shrink_factor + 1)
        elif self.zoom_factor is not None and self.shrink_factor is None:
            height_out = height_in_eff + (height_in_eff - 1) * (self.zoom_factor - 1)
            width_out = width_in_eff + (width_in_eff - 1) * (self.zoom_factor - 1)
        elif self.height is not None and self.width is not None:
            height_out = self.height
            width_out = self.width
        elif self.shrink_factor is not None and self.zoom_factor is not None:
            height_out = int((height_in_eff - 1) / self.shrink_factor + 1)
            width_out = int((width_in_eff - 1) / self.shrink_factor + 1)
            height_out = height_out + (height_out - 1) * (self.zoom_factor - 1)
            width_out = width_out + (width_out - 1) * (self.zoom_factor - 1)
        else:
            assert False, "Invalid params in interp_param"
        assert(height_in_eff > 0) 
        assert(width_in_eff > 0)
        assert(height_out > 0)
        assert(width_out > 0)
        num = input_shape[0]
        channels = input_shape[1]
        output_shape = [num, channels, height_out, width_out]
        return output_shape

    def forward(self, label):
        output_size = (self.height_out, self.width_out)
        #label[label==255] = 0
        if False: # check target
            targets = label.long().view(-1)
            ignore_label = 255
            num_classes = 21
            if True:
                if (targets[targets!=ignore_label] < 0).sum().item() > 0:
                    import pdb; pdb.set_trace()
                if (targets[targets!=ignore_label] >= num_classes).sum().item() > 0:
                    import pdb; pdb.set_trace()

                assert((targets[targets!=ignore_label] < 0).sum().item() == 0)
                assert((targets[targets!=ignore_label] >= num_classes).sum().item() == 0)

        return F.upsample(label.float(), size=output_size, mode='bilinear', align_corners=True)

    def __repr__(self):
        return "Interp()"


