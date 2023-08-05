#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

import tensorflow as tf

__author__ = 'cnheider'


def ensure_directory_exists(dir_name: str) -> None:
  '''
  Makes sure the folder exists on disk.

  Args:
    dir_name: Path string to the folder we want to create.
  '''
  if not os.path.exists(dir_name):
    os.makedirs(dir_name)


def get_image_path(*,
                   dataset,
                   label_name,
                   index,
                   set):
  '''
  Returns a path to an image for a label at the given index.

  Args:
    dataset: OrderedDict of images for each label.
    label_name: Label string we want to get an image for.
    index: Int offset of the image we want. This will be moduloed by the
    available number of images for the label, so it can be arbitrarily large.
    image_directory: Root folder string of the subfolders containing the training
    images.
    set: Name string of set to pull images from - training, testing, or
    validation.

  Returns:
    File system path string to an image that meets the requested parameters.

  '''
  if label_name not in dataset:
    tf.logging.fatal('Label does not exist %s.', label_name)
  label_lists = dataset[label_name]

  if set not in label_lists:
    tf.logging.fatal('Set does not exist %s.', set)
  set = label_lists[set]

  if not set:
    tf.logging.fatal('Label %s has no images in the category %s.',
                     label_name, set)

  mod_index = index % len(set)
  base_name = set[mod_index]

  return base_name


def get_embedding_path(dataset,
                       label_name,
                       index,
                       embedding_directory,
                       category,
                       module_name
                       ):
  '''
  Returns a path to a embedding file for a label at the given index.

  Args:
    dataset: OrderedDict of training images for each label.
    label_name: Label string we want to get an image for.
    index: Integer offset of the image we want. This will be moduloed by the
    available number of images for the label, so it can be arbitrarily large.
    embedding_directory: Folder string holding cached files of embedding values.
    category: Name string of set to pull images from - training, testing, or
    validation.
    module_name: The name of the image module being used.

  Returns:
    File system path string to an image that meets the requested parameters.
  '''
  module_name = (module_name.replace('://', '~')  # URL scheme.
                 .replace('/', '~')  # URL and Unix paths.
                 .replace(':', '~').replace('\\', '~'))  # Windows paths.

  i_path = get_image_path(dataset=dataset,
                 label_name=label_name,
                 index=index,
                 set=category)

  name = os.path.split(i_path)[1]

  e_path = f'{embedding_directory}/{label_name}/{name}'

  return e_path + '_' + module_name + '.txt'

def prepare_file_system(*,
                        summaries_directory,
                        intermediate_store_frequency,
                        intermediate_output_graphs_directory,
                        **kwargs):
  # Set up the directory we'll write summaries to for TensorBoard
  if tf.gfile.Exists(summaries_directory):
    pass
    # tf.gfile.DeleteRecursively(summaries_directory)
  else:
    tf.gfile.MakeDirs(summaries_directory)

  if intermediate_store_frequency > 0:
    ensure_directory_exists(intermediate_output_graphs_directory)
