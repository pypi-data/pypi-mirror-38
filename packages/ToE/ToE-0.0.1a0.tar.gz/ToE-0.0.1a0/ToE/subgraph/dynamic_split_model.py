import torch as t
import torch.nn as nn
import torch.nn.functional as F
from collections import OrderedDict


def ordered_dict_prepend(dct, key, value):
    dct.update({key: value})
    dct.move_to_end(key, last=False)


class MutableGraph(nn.Sequential):

    def pop(self, last=True):
        d = dict([])
        d['name'], d['module']=self._modules.popitem(last=last)
        return d

    def append(self, *args):
        if len(args) == 1 and isinstance(args[0], dict):
            self.add_module(args[0]['name'], args[0]['module'])
        else:
            self.add_module(*args)

    def prepend(self, *args):
        if len(args) == 1 and isinstance(args[0], dict):
            self.add_module(args[0]['name'], args[0]['module'])
            self._modules.move_to_end(args[0]['name'])
        else:
            self.add_module(*args)
            self._modules.move_to_end(args[0])


net = MutableGraph()