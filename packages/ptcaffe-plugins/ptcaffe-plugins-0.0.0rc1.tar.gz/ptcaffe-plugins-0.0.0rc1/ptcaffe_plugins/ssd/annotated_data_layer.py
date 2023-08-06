from __future__ import division, print_function

from ptcaffe.layer_dict import register_data_layer, CaffeData

@register_data_layer('AnnotatedData')
class AnnotatedData(CaffeData):
    def __init__(self, layer):
        super(AnnotatedData, self).__init__(layer)

    def get_batch_size(self):
        return int(self.layer['data_param']['batch_size'])
         
    def get_batch_num(self):
        import lmdb
        batch_size = int(self.layer['data_param']['batch_size'])
        lmdb_path = self.layer['data_param']['source']
        env = lmdb.open(lmdb_path)
        with env.begin() as txn:
            length = txn.stat()['entries']
        batch_num = int(length / batch_size)
        return batch_num

    def __repr__(self):
        return "AnnotatedData()"

