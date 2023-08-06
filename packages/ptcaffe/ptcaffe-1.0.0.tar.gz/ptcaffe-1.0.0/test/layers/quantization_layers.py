# encoding: UTF-8

from __future__ import division

import torch
import unittest
import ptcaffe.layers.quantization_layers as Q


class TestQRound(unittest.TestCase):
    def test_behavior(self):
        x = torch.arange(16).float() / 4
        r = Q.QRound.apply(x).data
        y = [float(round(i / 4)) for i in range(16)]
        self.assertEqual(r.tolist(), y)

    def test_empty(self):
        x = torch.zeros(0)
        r = Q.QRound.apply(x).data
        y = []
        self.assertEqual(r.tolist(), y)

    def test_scaler(self):
        x = torch.ones(1).squeeze() / 3
        r = Q.QRound.apply(x).data
        y = 0.
        self.assertEqual(r.tolist(), y)


class TestBitsToBase(unittest.TestCase):
    def test_behavior(self):
        excepted = {1: 1, 2: 3, 3: 7, 4: 15, 8: 255}
        for x, y in excepted.items():
            self.assertEqual(Q.bits_to_base(x), y)


class TestQuantize(unittest.TestCase):
    def test_behavior(self):
        # should quantize following numbers ...
        xs = 42 + torch.FloatTensor([
            0, 1 / 23, 1 / 17, 1 / 13, 1 / 11, 1 / 7, 1 / 5, 1 / 3, 5 / 14,
            1 / 2, 24 / 35, 29 / 35, 1
        ])
        qs = Q.quantize(xs, bits=3).data
        # ... to 42 + k / 7 where 0 <= k <= 7
        ys = 42 + torch.FloatTensor([
            0, 0, 0, 1 / 7, 1 / 7, 1 / 7, 1 / 7, 2 / 7, 3 / 7, 4 / 7, 5 / 7,
            6 / 7, 1
        ])
        self.assertEqual(float(qs.min()), float(xs.min()), msg='it should find out correct minimum')
        self.assertEqual(float(qs.max()), float(xs.max()), msg='it should find out correct maximum')
        self.assertEqual(len(set(qs.tolist())), 8, msg='it should map `xs` to a discrate value set')
        self.assertEqual(qs.tolist(), ys.tolist(), msg='it should quantize `xs` as excepted')


class TestStructure(unittest.TestCase):
    def test_inheritance(self):
        self.assertTrue(issubclass(Q.QConvolution, Q.QuantizationMixin))
        self.assertTrue(issubclass(Q.QInnerProduct, Q.QuantizationMixin))
        self.assertTrue(issubclass(Q.QPooling, Q.QuantizationMixin))
        self.assertTrue(issubclass(Q.QReLU, Q.QuantizationMixin))
        self.assertTrue(issubclass(Q.QConvolution, Q.QuantizeWeightsMixin))
        self.assertTrue(issubclass(Q.QInnerProduct, Q.QuantizeWeightsMixin))
