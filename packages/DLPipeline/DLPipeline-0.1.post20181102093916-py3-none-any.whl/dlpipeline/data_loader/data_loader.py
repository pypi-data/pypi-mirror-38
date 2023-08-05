#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from dlpipeline import prepare_file_system

from .dataset.image_list import build_first_level_image_list

__author__ = 'cnheider'

import tensorflow as tf
from collections.abc import Sequence


class DataLoader(Sequence):
  def __init__(self, C=None):
    super().__init__()
    self._dataset=None

    if C:
      self.load('', C)

  def load(self, param: str, C):
    if not C.image_directory:
      tf.logging.error('Must set flag --image_directory.')
      return -1

    prepare_file_system(**vars(C))  # Prepare necessary directories that can be used during training

    self._dataset = build_first_level_image_list(
      **vars(C))  # Look at the folder structure, and create lists of all the images.

    self._class_count = len(self._dataset.keys())
    if self._class_count == 0:
      tf.logging.error(f'No valid folders of images found at {C.image_directory}')
      return -1
    if self._class_count == 1:
      tf.logging.error(
          f'Only one valid folder of images found at {C.image_directory} - multiple classes are '
          f'needed for classification.')
      return -1

    return self

  @property
  def image_list(self):
    return self._dataset

  @property
  def class_count(self):
    return self._class_count

  def keys(self):
    return self._dataset.keys()

  def __iter__(self):
    return self.items()

  def items(self):
    return self._dataset.items()

  def __getitem__(self, item):
    return self._dataset.get(item)

  def __len__(self):
    return len(self.items())

  def __contains__(self, item):
    return self._dataset[item] is not None
