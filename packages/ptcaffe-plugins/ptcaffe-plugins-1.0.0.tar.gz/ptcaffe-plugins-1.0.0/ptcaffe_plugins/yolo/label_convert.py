import torch.nn as nn

class YoloTarget2SSDTarget(nn.Module):
    def __init__(self, layer, input_shape):
        super(YoloTarget2SSDTarget, self).__init__()

    def forward_shape(self, input_shape):
        return [1,1,1,7]

    def forward(self, yolo_target):
        cpu_target = yolo_target.cpu()
        ssd_target = []
        for b in range(cpu_target.shape[0]):
            for t in range(cpu_target.shape[1]//5):
                if cpu_target[b][t*5+1] == 0:
                    break
                l = cpu_target[b][t*5]
                cx = cpu_target[b][t*5+1]
                cy = cpu_target[b][t*5+2]
                ww = cpu_target[b][t*5+3]
                hh = cpu_target[b][t*5+4]
                x1 = cx - ww/2
                x2 = cx + ww/2
                y1 = cy - hh/2
                y2 = cy + hh/2
                ssd_target.append([b, l, -1, x1, y1, x2, y2, 0])
        ssd_target = torch.FloatTensor(ssd_target)
        ssd_target = ssd_target.to(target.device)
        return ssd_target
