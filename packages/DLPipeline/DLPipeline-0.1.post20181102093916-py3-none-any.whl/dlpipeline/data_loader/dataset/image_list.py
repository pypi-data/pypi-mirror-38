#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys

__author__ = 'cnheider'

import collections
import hashlib
import re
import tensorflow as tf

ACCEPTED_FORMATS = ['png', 'PNG', 'jpg', 'JPG', 'jpeg', 'JPEG', 'gif', 'GIF']

def build_first_level_image_list(*,
                                 image_directory,
                                 testing_percentage=0.15,
                                 validation_percentage=0.15,
                                 **kwargs):
  '''
  Builds a list of training images from the file system.

  Analyzes the sub folders in the image directory, splits them into stable
  training, testing, and validation sets, and returns a data structure
  describing the lists of images for each label and their paths.

  Args:
    image_directory: String path to a folder containing subfolders of images.
    testing_percentage: Integer percentage of the images to reserve for tests.
    validation_percentage: Integer percentage of images reserved for validation.

  Returns:
    An OrderedDict containing an entry for each label subfolder, with images
    split into training, testing, and validation sets within each label.
    The order of items defines the class indices.
  '''

  if not tf.gfile.Exists(image_directory):
    dir_err = f"Image directory {image_directory} not found."
    tf.logging.error(dir_err)
    print(dir_err)
    return None

  result = collections.OrderedDict()

  class_directories = next(tf.gfile.Walk(image_directory))[1]

  classes = {label:[] for label in class_directories}

  for class_directory in classes:
    a = [x[0] for x in tf.gfile.Walk(os.path.join(image_directory, class_directory))]
    sub_directories = sorted(a)

    for sub_directory in sub_directories:
      tf.logging.info(f"Looking for images in {sub_directory}")

      file_extensions = sorted(set(os.path.normcase(ext)
                                   for ext in ACCEPTED_FORMATS))

      for extension in file_extensions:
        file_glob = os.path.join(sub_directory, '*.' + extension)
        this_glob = tf.gfile.Glob(file_glob)
        classes[class_directory].extend(this_glob)

  for label in classes:
    training_images = []
    testing_images = []
    validation_images = []

    for file_name in classes[label]:

      hash_name = re.sub(r'_nohash_.*$', '', file_name)
      hash_name_hashed = hashlib.sha1(tf.compat.as_bytes(hash_name)).hexdigest()
      percentage_hash = ((int(hash_name_hashed, 16) %
                          (sys.maxsize + 1)) *
                         (100.0 / sys.maxsize))

      if percentage_hash < validation_percentage:
        validation_images.append(file_name)
      elif percentage_hash < (testing_percentage + validation_percentage):
        testing_images.append(file_name)
      else:
        training_images.append(file_name)

      result[label] = {
        'training':  training_images,
        'testing':   testing_images,
        'validation':validation_images,
        }

  return result
