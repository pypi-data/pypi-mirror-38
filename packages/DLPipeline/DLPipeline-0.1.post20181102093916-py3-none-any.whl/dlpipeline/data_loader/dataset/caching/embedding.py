#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import random
import sys

from dlpipeline.utilities.path_utilities import ensure_directory_exists, get_embedding_path, get_image_path

__author__ = 'cnheider'

import tensorflow as tf
import numpy as np


def get_or_create_embedding(sess,
                            dataset,
                            label_name,
                            index,
                            category,
                            embedding_directory,
                            jpeg_data_tensor,
                            decoded_image_tensor,
                            resized_input_tensor,
                            embedding_node,
                            embedding_module
                            ):
  '''Retrieves or calculates embedding values for an image.

  If a cached version of the embedding data exists on-disk, return that,
  otherwise calculate the data and save it to disk for future use.

  Args:
    sess: The current active TensorFlow Session.
    dataset: OrderedDict of training images for each label.
    label_name: Label string we want to get an image for.
    index: Integer offset of the image we want. This will be modulo-ed by the
    available number of images for the label, so it can be arbitrarily large.
    category: Name string of which set to pull images from - training, testing,
    or validation.
    embedding_directory: Folder string holding cached files of embedding values.
    jpeg_data_tensor: The tensor to feed loaded jpeg data into.
    decoded_image_tensor: The output of decoding and resizing the image.
    resized_input_tensor: The input node of the recognition graph.
    embedding_node: The output tensor for the embedding values.
    embedding_module: The name of the image module being used.

  Returns:
    Numpy array of values produced by the embedding layer for the image.
  '''

  sub_directory_path = os.path.join(embedding_directory, label_name)
  ensure_directory_exists(sub_directory_path)
  embedding_file_path = get_embedding_path(dataset,
                                      label_name,
                                      index,
                                      embedding_directory,
                                      category,
                                      embedding_module)

  if not os.path.exists(embedding_file_path):
    create_embedding_file(embedding_file_path,
                          dataset,
                          label_name,
                          index,
                          category,
                          sess,
                          jpeg_data_tensor,
                          decoded_image_tensor,
                          resized_input_tensor,
                          embedding_node)

  with open(embedding_file_path, 'r') as embedding_file:
    embedding_string = embedding_file.read()

  did_hit_error = False
  embedding_values = None

  try:
    embedding_values = [float(x) for x in embedding_string.split(',')]
  except ValueError:
    tf.logging.warning('Invalid float found, recreating embedding')
    did_hit_error = True

  if did_hit_error:
    create_embedding_file(embedding_file_path,
                          dataset,
                          label_name,
                          index,
                          category,
                          sess,
                          jpeg_data_tensor,
                          decoded_image_tensor,
                          resized_input_tensor,
                          embedding_node)

    with open(embedding_file_path, 'r') as embedding_file:
      embedding_string = embedding_file.read()
    # Allow exceptions to propagate here, since they shouldn't happen after a
    # fresh creation
    embedding_values = [float(x) for x in embedding_string.split(',')]

  return embedding_values


def run_embedding_on_image(sess,
                           image_data,
                           image_data_tensor,
                           decoded_image_tensor,
                           resized_input_tensor,
                           embedding_node):
  '''Runs inference on an image to extract the 'embedding' summary layer.

  Args:
    sess: Current active TensorFlow Session.
    image_data: String of raw JPEG data.
    image_data_tensor: Input data layer in the graph.
    decoded_image_tensor: Output of initial image resizing and preprocessing.
    resized_input_tensor: The input node of the recognition graph.
    embedding_node: Layer before the final softmax.

  Returns:
    Numpy array of embedding values.
  '''
  # First decode the JPEG image, resize it, and rescale the pixel values.
  resized_input_values = sess.run(decoded_image_tensor,
                                  {image_data_tensor:image_data})
  # Then run it through the recognition network.
  embedding_values = sess.run(embedding_node,
                              {resized_input_tensor:resized_input_values})
  embedding_values = np.squeeze(embedding_values)
  return embedding_values


def create_embedding_file(embedding_path,
                          dataset,
                          label_name,
                          index,
                          category,
                          sess,
                          jpeg_data_tensor,
                          decoded_image_tensor,
                          resized_input_tensor,
                          embedding_node
                          ):
  '''Create a single embedding file.'''
  print('Creating embedding at ' + embedding_path)
  image_path = get_image_path(dataset=dataset,
                              label_name=label_name,
                              index=index,
                              set=category)
  if not tf.gfile.Exists(image_path):
    tf.logging.fatal('File does not exist %s', image_path)

  image_data = tf.gfile.FastGFile(image_path, 'rb').read()

  try:
    embedding_values = run_embedding_on_image(
        sess, image_data, jpeg_data_tensor, decoded_image_tensor,
        resized_input_tensor, embedding_node)
  except Exception as e:
    raise RuntimeError('Error during processing file %s (%s)' % (image_path,
                                                                 str(e)))

  embedding_string = ','.join(str(x) for x in embedding_values)

  with open(embedding_path, 'w') as embedding_file:
    embedding_file.write(embedding_string)


def cache_embeddings(sess,
                     dataset,
                     jpeg_data_tensor,
                     decoded_image_tensor,
                     resized_input_tensor,
                     embedding_node,
                     *,
                     embedding_directory,
                     embedding_module,
                     **kwargs):
  '''Ensures all the training, testing, and validation embeddings are cached.

  Because we're likely to read the same image multiple times (if there are no
  distortions applied during training) it can speed things up a lot if we
  calculate the embedding layer values once for each image during
  preprocessing, and then just read those cached values repeatedly during
  training. Here we go through all the images we've found, calculate those
  values, and save them off.

  Args:
    sess: The current active TensorFlow Session.
    dataset: OrderedDict of training images for each label.
    image_directory: Root folder string of the subfolders containing the training
    images.
    embedding_directory: Folder string holding cached files of embedding values.
    jpeg_data_tensor: Input tensor for jpeg data from file.
    decoded_image_tensor: The output of decoding and resizing the image.
    resized_input_tensor: The input node of the recognition graph.
    embedding_node: The penultimate output layer of the graph.
    embedding_module: The name of the image module being used.

  Returns:
    Nothing.
  '''
  how_many_embeddings = 0
  ensure_directory_exists(embedding_directory)

  for label_name, label_lists in dataset.items():
    for category in ['training', 'testing', 'validation']:
      category_list = label_lists[category]

      for index, unused_base_name in enumerate(category_list):
        get_or_create_embedding(
            sess,
            dataset,
            label_name,
            index,
            category,
            embedding_directory,
            jpeg_data_tensor,
            decoded_image_tensor,
            resized_input_tensor,
            embedding_node,
            embedding_module)

        how_many_embeddings += 1
        if how_many_embeddings % 100 == 0:
          tf.logging.info(
              str(how_many_embeddings) + ' embedding files created.')


def get_random_cached_embeddings(sess,
                                 dataset,
                                 category,
                                 jpeg_data_tensor,
                                 decoded_image_tensor,
                                 resized_input_tensor,
                                 embedding_node,
                                 *,
                                 embedding_directory,
                                 batch_size,
                                 embedding_module,
                                 **kwargs
                                 ):
  '''Retrieves embedding values for cached images.

  If no distortions are being applied, this function can retrieve the cached
  embedding values directly from disk for images. It picks a random set of
  images from the specified category.

  Args:
    sess: Current TensorFlow Session.
    dataset: OrderedDict of training images for each label.
    batch_size: If positive, a random sample of this size will be chosen.
    If negative, all embeddings will be retrieved.
    category: Name string of which set to pull from - training, testing, or
    validation.
    embedding_directory: Folder string holding cached files of embedding values.
    image_directory: Root folder string of the subfolders containing the training
    images.
    jpeg_data_tensor: The layer to feed jpeg image data into.
    decoded_image_tensor: The output of decoding and resizing the image.
    resized_input_tensor: The input node of the recognition graph.
    embedding_node: The embedding output layer of the CNN graph.
    embedding_module: The name of the image module being used.

  Returns:
    List of embedding arrays, their corresponding ground truths, and the
    relevant filenames.
  '''
  embeddings = []
  ground_truths = []
  filenames = []
  if batch_size >= 0:
    # Retrieve a random sample of embeddings.
    for unused_i in range(batch_size):
      label_index = random.randrange(dataset.class_count)
      label_name = list(dataset.keys())[label_index]
      image_index = random.randrange(sys.maxsize + 1)
      image_name = get_image_path(dataset=dataset,
                                  label_name=label_name,
                                  index=image_index,
                                  set=category)

      embedding = get_or_create_embedding(
          sess,
          dataset,
          label_name,
          image_index,
          category,
          embedding_directory,
          jpeg_data_tensor,
          decoded_image_tensor,
          resized_input_tensor,
          embedding_node,
          embedding_module)
      embeddings.append(embedding)
      ground_truths.append(label_index)
      filenames.append(image_name)
  else:
    # Retrieve all embeddings.
    for label_index, label_name in enumerate(dataset.keys()):
      for image_index, image_name in enumerate(dataset[label_name][category]):
        image_name = get_image_path(dataset=dataset,
                                    label_name=label_name,
                                    index=image_index,
                                    set=category)
        embedding = get_or_create_embedding(sess,
                                            dataset,
                                            label_name,
                                            image_index,
                                            category,
                                            embedding_directory,
                                            jpeg_data_tensor,
                                            decoded_image_tensor,
                                            resized_input_tensor,
                                            embedding_node,
                                            embedding_module
                                            )
        embeddings.append(embedding)
        ground_truths.append(label_index)
        filenames.append(image_name)
  return embeddings, ground_truths, filenames


def get_random_distorted_embeddings_online(
    sess,
    dataset,
    category,
    input_jpeg_tensor,
    distorted_image,
    resized_input_tensor,
    embedding_node,
    *,
    batch_size,
    **kwargs
    ):
  '''
  Retrieves embedding values for training images, after distortions.

  If we're training with distortions like crops, scales, or flips, we have to
  recalculate the full classifier for every image, and so we can't use cached
  embedding values. Instead we find random images for the requested category,
  run them through the distortion graph, and then the full graph to get the
  embedding results for each.

  Args:
    sess: Current TensorFlow Session.
    dataset: OrderedDict of training images for each label.
    how_many: The integer number of embedding values to return.
    category: Name string of which set of images to fetch - training, testing,
    or validation.
    image_directory: Root folder string of the subfolders containing the training
    images.
    input_jpeg_tensor: The input layer we feed the image data to.
    distorted_image: The output node of the distortion graph.
    resized_input_tensor: The input node of the recognition graph.
    embedding_node: The embedding output layer of the CNN graph.

  Returns:
    List of embedding arrays and their corresponding ground truths.
    :param sess:
    :param dataset:
    :param category:
    :param input_jpeg_tensor:
    :param distorted_image:
    :param resized_input_tensor:
    :param embedding_node:
    :param batch_size:
  '''
  embeddings = []
  ground_truths = []
  for unused_i in range(batch_size):
    label_index = random.randrange(dataset.class_count)
    label_name = list(dataset.keys())[label_index]
    image_index = random.randrange(sys.maxsize + 1)
    image_path = get_image_path(dataset=dataset,
                                label_name=label_name,
                                index=image_index,
                                set=category)
    if not tf.gfile.Exists(image_path):
      tf.logging.fatal('File does not exist %s', image_path)
    jpeg_data = tf.gfile.FastGFile(image_path, 'rb').read()
    # Note that we materialize the distorted_image_data as a numpy array before
    # sending running inference on the image. This involves 2 memory copies and
    # might be optimized in other implementations.
    distorted_image_data = sess.run(distorted_image,
                                    {input_jpeg_tensor:jpeg_data})
    embedding_values = sess.run(embedding_node,
                                {resized_input_tensor:distorted_image_data})
    embedding_values = np.squeeze(embedding_values)
    embeddings.append(embedding_values)
    ground_truths.append(label_index)
  return embeddings, ground_truths
