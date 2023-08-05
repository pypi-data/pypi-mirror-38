#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from dlpipeline.augmentor.tf_augmentor import TFAugmentor

__author__ = 'cnheider'


class Model(object):
  def __init__(self, dataset: iter, transformer: TFAugmentor, C):
    super().__init__()

  def learn(self, dataset: iter, C=None):
    raise NotImplementedError

  def predict(self, param: iter):
    raise NotImplementedError

  def summary(self):
    raise NotImplementedError

  def save(self, dataset, C):
    raise NotImplementedError

  def test(self, dataset, C):
    raise NotImplementedError
