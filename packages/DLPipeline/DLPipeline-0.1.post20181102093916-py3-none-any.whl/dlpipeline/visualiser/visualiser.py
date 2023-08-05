#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'cnheider'

import tensorflow as tf

class Visualiser(object):
  def __init__(self,C=None):
    super().__init__()

  def visualise(self, results):
    pass

  def make_variable_summary(self, variable):
    '''Attach a lot of summaries to a Tensor (for TensorBoard visualization).'''
    with tf.name_scope('summaries'):
      mean = tf.reduce_mean(variable)
      tf.summary.scalar('mean', mean)
      with tf.name_scope('stddev'):
        stddev = tf.sqrt(tf.reduce_mean(tf.square(variable - mean)))
      tf.summary.scalar('stddev', stddev)
      tf.summary.scalar('max', tf.reduce_max(variable))
      tf.summary.scalar('min', tf.reduce_min(variable))
      tf.summary.histogram('histogram', variable)
