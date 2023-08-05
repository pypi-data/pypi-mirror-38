#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from dlpipeline.visualiser.visualiser import Visualiser

__author__ = 'cnheider'

import tensorflow as tf


def add_additional_retraining_nodes(*,
                                    embedding_node,
                                    input_size,
                                    output_size,
                                    is_training,
                                    batch_size=None,
                                    output_node_name='softmax_output',
                                    learning_rate=0,
                                    quantize=False,
                                    stddev=0.001,
                                    **kwargs):
  '''
  Adds a new softmax and fully-connected layer for training and eval.

  We need to retrain the top layer to identify our new classes, so this function
  adds the right operations to the graph, along with some variables to hold the
  weights, and then sets up all the gradients for the backward pass.

  The set up for the softmax and fully-connected layers is based on:
  https://www.tensorflow.org/tutorials/mnist/beginners/index.html

  Args:
    class_count: Integer of how many categories of things we're trying to
        recognize.
    final_node_name: Name string for the new final node that produces results.
    embedding_node: The output of the main CNN graph.
    quantize_layer: Boolean, specifying whether the newly added layer should be
        instrumented for quantization with TF-Lite.
    is_training: Boolean, specifying whether the newly add layer is for training
        or eval.

  Returns:
    The tensors for the training and cross entropy results, and tensors for the
    embedding input and ground truth input.
    :param embedding_node:
    :param output_size:
    :param input_size:
    :param quantize:
    :param is_training:
    :param output_node_name:
    :param learning_rate:
  '''

  assert batch_size is None

  with tf.name_scope('DataInput'):
    input_node = tf.placeholder_with_default(embedding_node,
                                             shape=[batch_size,
                                                    input_size
                                                    ],
                                             name='InputPlaceholder'
                                             )

    label_node = tf.placeholder(tf.int64, [batch_size], name='LabelPlaceholder')

  with tf.name_scope('retraining_operations'):
    '''
    with tf.name_scope('weights1'):
      initial_value = tf.truncated_normal([input_size, output_size], stddev=stddev)
      layer_weights = tf.Variable(initial_value, name='retraining_weights')
      Visualiser.make_variable_summary(Visualiser(), layer_weights)

    with tf.name_scope('biases1'):
      layer_biases = tf.Variable(tf.zeros([output_size]), name='retraining_biases')
      Visualiser.make_variable_summary(Visualiser(), layer_biases)

    with tf.name_scope('Wx_plus_b1'):
      interm = tf.matmul(input_node, layer_weights) + layer_biases
      tf.summary.histogram('interm', interm)
    
    '''
    with tf.name_scope('weights'):
      initial_value = tf.truncated_normal([input_size, output_size], stddev=stddev)
      layer_weights = tf.Variable(initial_value, name='retraining_weights')
      Visualiser.make_variable_summary(Visualiser(), layer_weights)

    with tf.name_scope('biases'):
      layer_biases = tf.Variable(tf.zeros([output_size]), name='retraining_biases')
      Visualiser.make_variable_summary(Visualiser(), layer_biases)

    with tf.name_scope('Wx_plus_b'):
      logits = tf.matmul(input_node, layer_weights) + layer_biases
      tf.summary.histogram('logits', logits)

  softmax_node = tf.nn.softmax(logits, name=output_node_name)

  if quantize:
    if is_training:
      tf.quantize.create_training_graph()
    else:
      tf.quantize.create_eval_graph()

  tf.summary.histogram(f'{output_node_name}_activations', softmax_node)

  if not is_training:  # If this is an eval graph, we don't need to add loss ops or an optimizer.
    return None, None, input_node, label_node, softmax_node

  cross_entropy_scope = 'cross_entropy_loss'
  with tf.name_scope(cross_entropy_scope):
    cross_entropy_mean_node = tf.losses.sparse_softmax_cross_entropy(labels=label_node, logits=logits)

  tf.summary.scalar(cross_entropy_scope, cross_entropy_mean_node)

  with tf.name_scope('optimiser'):
    optimizer = tf.train.GradientDescentOptimizer(learning_rate)
    train_step_node = optimizer.minimize(cross_entropy_mean_node)

  return (train_step_node,
          cross_entropy_mean_node,
          input_node,
          label_node,
          softmax_node)


def add_evaluation_nodes(*,result_node, ground_truth_node):
  '''Inserts the operations we need to evaluate the accuracy of our results.

  Args:
    result_node: The new final node that produces results.
    ground_truth_node: The node we feed ground truth data
    into.

  Returns:
    Tuple of (evaluation step, prediction).
  '''
  with tf.name_scope('accuracy'):
    with tf.name_scope('correct_prediction'):
      prediction_node = tf.argmax(result_node, 1)
      correct_prediction = tf.equal(ground_truth_node,prediction_node)
      cf_mat = tf.confusion_matrix(ground_truth_node,prediction_node)
    with tf.name_scope('accuracy'):
      evaluation_step_node = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

  tf.summary.scalar('accuracy', evaluation_step_node)

  return (evaluation_step_node,
          prediction_node,
          cf_mat)

