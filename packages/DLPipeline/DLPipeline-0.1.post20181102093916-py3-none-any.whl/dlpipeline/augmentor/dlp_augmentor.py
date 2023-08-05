#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'cnheider'


class DLPAugmentor(object):
  def __init__(self, C):
    super().__init__()

    self._preprocess = (C.flip_left_right_p or (C.random_crop_p != 0) or (C.random_scale_p != 0) or
                        (C.random_brightness_p != 0))

  def transform(self,
                graph,
                module_spec,
                dataset,
                resized_image_node,
                embedding_node,
                C):
    pass


  @property
  def preprocess(self):
    return self._preprocess
