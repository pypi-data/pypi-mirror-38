from __future__ import division, print_function

import copy
from collections import OrderedDict

import torch
import torch.nn as nn


class RandomData(nn.Module):
    def __init__(self, layer):
        super(RandomData, self).__init__()
        data_param = layer.get('data_param', OrderedDict())
        input_dims = data_param['input_dim']
        self.dims = [int(dim) for dim in input_dims]

    def forward(self):
        return torch.randn(self.dims)

    def forward_shape(self):
        return copy.copy(self.dims)
