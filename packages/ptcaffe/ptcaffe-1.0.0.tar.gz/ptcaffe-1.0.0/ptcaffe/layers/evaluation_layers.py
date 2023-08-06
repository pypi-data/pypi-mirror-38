# --------------------------------------------------------
# ptcaffe
# Licensed under The MIT License [see LICENSE for details]
# Written by xiaohang
# --------------------------------------------------------

from __future__ import division, print_function

import abc

import torch.nn as nn
import threading
from ptcaffe.utils.logger import logger
from collections import OrderedDict
from .evaluation_metrics import AccuracyMetric

__all__ = ['BaseEvaluator', 'AccuracyEvaluator', 'Accuracy']


class BaseEvaluator(nn.Module):
    def __init__(self, layer, *input_shapes):
        super(BaseEvaluator, self).__init__()
        phase = layer['include']['phase']
        assert phase == 'TEST', "Evaluator should be in TEST phase"
        self.metric = self.create_metric(layer, *input_shapes)
        self.lock = threading.Lock()
        self.device = -1
        self.devices = [-1]

    def __repr__(self):
        return "BaseEvaluator()"

    @abc.abstractmethod
    def create_metric(self, layer, *input_shapes):
        pass

    def set_devices(self, devices):
        self.devices = devices

    def set_device(self, device):
        self.device = device

    def forward_shape(self, *input_shapes):
        pass

    def reset_metric(self):
        if self.device == self.devices[0]:
            result = self.metric.get()
            if isinstance(result, float):
                logger.info('evaluation result : %f' % float(result))
            elif isinstance(result, (list, tuple)):
                for i, val in enumerate(result):
                    logger.info('evaluation result%d : %f' % (i, val))
            elif isinstance(result, (dict, OrderedDict)):
                for key, val in result.items():
                    logger.info('%s: %f' % (key, val))

            self.metric.reset()

    def forward(self, *inputs):
        self.lock.acquire()
        self.metric.update(*inputs)
        self.lock.release()


class AccuracyEvaluator(BaseEvaluator):
    def __init__(self, layer, *input_shapes):
        super(AccuracyEvaluator, self).__init__(layer, *input_shapes)

    def create_metric(self, layer, *input_shapes):
        evaluator_param = layer.get('evaluator_param', OrderedDict())
        top_k = int(evaluator_param.get('top_k', 1))
        ignore_label = None
        if 'ignore_label' in evaluator_param:
            ignore_label = int(evaluator_param['ignore_label'])
        metric = AccuracyMetric(top_k, ignore_label)
        return metric

    def __repr__(self):
        return 'AccuracyEvaluator()'


class Accuracy(nn.Module):
    def __init__(self, layer, *input_shapes):
        super(Accuracy, self).__init__()
        accuracy_param = layer.get('accuracy_param', OrderedDict())
        self.top_k = int(accuracy_param.get('top_k', 1))
        self.ignore_label = None
        if 'ignore_label' in accuracy_param:
            self.ignore_label = int(accuracy_param['ignore_label'])

    def __repr__(self):
        return 'Accuracy()'

    def forward_shape(self, input_shape1, input_shape2):
        return [1, ]

    def forward(self, output, label):
        if self.top_k == 1:
            if self.ignore_label is None:
                max_vals, max_ids = output.data.max(1)
                if label.dim() > 1 and label.numel() == output.size(0):
                    label = label.view(-1)
                n_correct = (max_ids.view(-1).long() == label.data.long()).sum()
                batchsize = output.data.size(0)
                accuracy = float(n_correct) / batchsize
                accuracy = output.data.new().resize_(1).fill_(accuracy)
                return accuracy
            else:
                max_vals, max_ids = output.data.max(1)
                non_ignore_mask = (label.data.long() != self.ignore_label)
                n_correct = ((max_ids.view(-1).long() == label.data.long()) & non_ignore_mask).sum()
                non_ignore_num = float(non_ignore_mask.sum())
                accuracy = float(n_correct) / (non_ignore_num + 1e-6)
                accuracy = output.data.new().resize_(1).fill_(accuracy)
                return accuracy
        else:
            assert self.top_k == 5
            max_vals, max_ids = output.data.topk(self.top_k, 1)
            label_size = label.numel()
            label_ext = label.data.long().view(label_size, 1).expand(label_size, self.top_k)
            compare = (max_ids.view(-1, self.top_k) == label_ext)
            n_correct = compare.sum()
            batchsize = output.data.size(0)
            accuracy = float(n_correct) / batchsize
            accuracy = output.data.new().resize_(1).fill_(accuracy)
            return accuracy
