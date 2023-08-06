from .upsample_layer import YoloUpsample
from .reorg_layer import Reorg
from .eval_layers import Yolov2Recall, Yolov2Valid
from .region_loss import RegionLossWrapper
from .yolo_loss import YoloLossWrapper
from .data_layer import Yolo2ListData
from .label_convert import YoloTarget2SSDTarget

from ptcaffe.layer_dict import add_data_layer, add_loss_layer, add_layer

add_data_layer('Yolo2ListData', Yolo2ListData)
add_loss_layer('RegionLoss', RegionLossWrapper)
add_loss_layer('YoloLoss', YoloLossWrapper)
add_layer('Yolov2Recall', Yolov2Recall)
add_layer('Yolov2Valid', Yolov2Valid)
add_layer('Reorg', Reorg)
add_layer('YoloUpsample', YoloUpsample)
add_layer('YoloTarget2SSDTarget', YoloTarget2SSDTarget)
