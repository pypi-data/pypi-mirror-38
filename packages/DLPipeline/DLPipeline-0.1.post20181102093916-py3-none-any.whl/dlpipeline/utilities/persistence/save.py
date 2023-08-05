#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from dlpipeline.classifier.evaluation import build_eval_session

__author__ = 'cnheider'

import tensorflow as tf


def save_graph_to_file(graph_file_name,
                       module_spec,
                       class_count,

                       checkpoint_name,
                                              ):
  '''
  Saves an graph to file, creating a valid quantized one if necessary.
  '''
  sess, _, _, _, _, _ = build_eval_session(module_spec,
                                           class_count,
                                           checkpoint_name,
                                           )
  graph = sess.graph

  output_graph_def = tf.graph_util.convert_variables_to_constants(
      sess, graph.as_graph_def(), ['softmax_output'])

  with tf.gfile.FastGFile(graph_file_name, 'wb') as f:
    f.write(output_graph_def.SerializeToString())
