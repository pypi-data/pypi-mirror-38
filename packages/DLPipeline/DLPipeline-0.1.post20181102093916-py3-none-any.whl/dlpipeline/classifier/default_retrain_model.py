#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from dlpipeline.classifier.cf_mat import plot_confusion_matrix
from dlpipeline.data_loader.dataset.caching.embedding import (get_random_distorted_embeddings_online,
                                                              get_random_cached_embeddings,
                                                              )
from dlpipeline.classifier.add_layers import add_additional_retraining_nodes, add_evaluation_nodes
from dlpipeline.classifier.evaluation import run_final_eval
from dlpipeline.classifier.model import Model
from dlpipeline.augmentor.tf_augmentor import TFAugmentor
from dlpipeline.utilities.persistence.export import export_model
from dlpipeline.utilities.persistence.save import save_graph_to_file

__author__ = 'cnheider'

from datetime import datetime

import tensorflow as tf


class DefaultRetrainModel(Model):
  def __init__(self, dataset: iter, transformer: TFAugmentor, C):
    super().__init__(dataset, transformer, C)

    self._transformer = transformer

    (self._graph,
     self._embedding_node,
     self._resized_image_node,
     self._quantize,
     self._module_spec) = transformer.load_hub_module(C)

    batch_size, embedding_size = self._embedding_node.get_shape().as_list()

    with self._graph.as_default():
      (self._train_step_node,
       self._cross_entropy_node,
       self._input_node,
       self._label_node,
       self._prediction_node) = add_additional_retraining_nodes(embedding_node=self._embedding_node,
                                                                input_size=embedding_size,
                                                                output_size=dataset.class_count,
                                                                batch_size=batch_size,
                                                                is_training=True,
                                                                learning_rate=C.learning_rate)

    # endregion

    (self._jpeg_node,
     self._decoded_image_node,
     self._distorted_jpeg_node,
     self._distorted_image_node) = transformer.add_transformation_nodes(self._graph,
                                                                        self._module_spec,
                                                                        dataset,
                                                                        self._resized_image_node,
                                                                        self._embedding_node, C)

  def fetch_data(self, sess, dataset, C, sub_set='training'):
    '''
    Get a batch of input embedding values, either calculated fresh every
     time with distortions applied, or from the cache stored on disk.
    '''
    if self._transformer.preprocess:
      (features, label) = get_random_distorted_embeddings_online(sess,
                                                                 dataset,
                                                                 sub_set,
                                                                 self._distorted_jpeg_node,
                                                                 self._distorted_image_node,
                                                                 self._resized_image_node,
                                                                 self._embedding_node,
                                                                 batch_size=C.train_batch_size,
                                                                 image_directory=C.image_directory
                                                                 )
    else:
      (features, label, _) = get_random_cached_embeddings(sess,
                                                          dataset,
                                                          sub_set,
                                                          self._jpeg_node,
                                                          self._decoded_image_node,
                                                          self._resized_image_node,
                                                          self._embedding_node,
                                                          embedding_module=C.embedding_module,
                                                          batch_size=C.train_batch_size,
                                                          embedding_directory=C.embedding_directory,
                                                          image_directory=C.image_directory)

    return features, label

  def learn(self, dataset: iter, C=None):
    # Needed to make sure the logging output is visible.
    # See https://github.com/tensorflow/tensorflow/issues/3047
    tf.logging.set_verbosity(tf.logging.INFO)

    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True

    with tf.Session(config=config, graph=self._graph) as sess:
      sess.run(tf.global_variables_initializer())

      train_saver = tf.train.Saver()

      # Create the operations we need to evaluate the accuracy of our new layer.
      evaluation_node, _, cfm_node, *_ = add_evaluation_nodes(result_node=self._prediction_node,
                                                              ground_truth_node=self._label_node
                                                              )

      merged_summaries = tf.summary.merge_all()

      train_writer = tf.summary.FileWriter(C.summaries_directory + 'training_set', sess.graph)
      validation_writer = tf.summary.FileWriter(C.summaries_directory + 'validation_set')

      # Run the training for as many cycles as requested on the command line.
      for step_i in range(C.steps):

        (features, labels) = self.fetch_data(sess, dataset, C)

        train_summary, _ = sess.run([merged_summaries, self._train_step_node],
                                    feed_dict={self._input_node:features,
                                               self._label_node:labels
                                               }
                                    )

        train_writer.add_summary(train_summary, step_i)

        if (step_i % C.eval_step_interval) == 0 or step_i + 1 == C.steps:
          train_accuracy, cross_entropy_value, cf_mat_value = sess.run([evaluation_node,
                                                                        self._cross_entropy_node,
                                                                        cfm_node],
                                                                       feed_dict={
                                                                         self._input_node:features,
                                                                         self._label_node:labels
                                                                         }
                                                                       )

          conf_mat = plot_confusion_matrix(None,
                                           None,
                                           ['positive', 'negative'],
                                           tensor_name='training/confusion_matrix',
                                           cm=cf_mat_value)
          train_writer.add_summary(conf_mat, step_i)


          tf.logging.info(f'{datetime.now()}: Step {step_i:d}: Train accuracy = {train_accuracy * 100:.1f}%%')
          tf.logging.info(f'{datetime.now()}: Step {step_i:d}: Cross entropy = {cross_entropy_value:f}')
          tf.logging.info(f'{datetime.now()}: Step {step_i:d}: Confusion Matrix = {cf_mat_value}')

          (validation_embeddings,
           validation_label,
           _) = get_random_cached_embeddings(sess,
                                             dataset,
                                             'validation',
                                             self._jpeg_node,
                                             self._decoded_image_node,
                                             self._resized_image_node,
                                             self._embedding_node,
                                             embedding_module=C.embedding_module,
                                             batch_size=C.validation_batch_size,
                                             embedding_directory=C.embedding_directory,
                                             image_directory=C.image_directory
                                             )

          (validation_summary,
           validation_accuracy,
           validation_cf_mat_value) = sess.run([merged_summaries,
                                            evaluation_node
                                            ,cfm_node],
                                           feed_dict={
                                             self._input_node:validation_embeddings,
                                             self._label_node:validation_label
                                             }
                                           )

          validation_writer.add_summary(validation_summary, step_i)
          tf.logging.info(
              f'{datetime.now()}: '
              f'Step {step_i:d}: Validation accuracy = {validation_accuracy * 100:.1f}%% '
              f'(N={len(validation_embeddings):d})')

          val_conf_mat = plot_confusion_matrix(None,
                                           None,
                                           ['positive', 'negative'],
                                           tensor_name='validation/confusion_matrix',
                                           cm=validation_cf_mat_value)
          validation_writer.add_summary(val_conf_mat, step_i)

        if C.intermediate_store_frequency > 0 and (
            step_i % C.intermediate_store_frequency == 0) and step_i > 0:
          self.intermediate_save(step_i, dataset.class_count, train_saver, sess, C)

      # endregion

      train_saver.save(sess,
                       C.checkpoint_name)  # After training is complete, force one last save of the train
    # checkpoint.

  def predict(self, param: iter):
    pass

  def summary(self):
    pass

  def intermediate_save(self, i, class_count, train_saver, sess, C):
    # If we want to do an intermediate save,
    # save a checkpoint of the train graph, to restore into
    # the eval graph.
    train_saver.save(sess, C.checkpoint_name)

    intermediate_file_name = (C.intermediate_output_graphs_directory +
                              'intermediate_' + str(i) + '.pb')

    tf.logging.info(f'Save intermediate result to : {intermediate_file_name}')

    save_graph_to_file(intermediate_file_name,
                       self._module_spec,
                       class_count,
                       C.checkpoint_name)

  def save(self, dataset, C):

    # Write out the trained graph and labels with the weights stored as constants.
    tf.logging.info(f'Save final result to : {C.output_graph}')
    if self._quantize:
      tf.logging.info('The classifier is instrumented for quantization with TF-Lite')

    save_graph_to_file(C.output_graph,
                       self._module_spec,
                       dataset.class_count,
                       C.checkpoint_name)

    with tf.gfile.FastGFile(C.output_labels, 'w') as f:
      f.write('\n'.join(dataset.keys()) + '\n')

    if C.saved_model_directory:
      export_model(self._module_spec, dataset.class_count, **vars(C))

  def test(self, dataset, C):
    with tf.Session(graph=self._graph) as sess:
      run_final_eval(sess,
                     self._module_spec,
                     dataset,
                     self._jpeg_node,
                     self._decoded_image_node,
                     self._resized_image_node,
                     self._embedding_node,

                     **vars(C))
