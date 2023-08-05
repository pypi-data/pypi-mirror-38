#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from albumentations import (Blur, CLAHE, Compose, Flip, GaussNoise, GridDistortion, HueSaturationValue,
                            IAAAdditiveGaussianNoise, IAAEmboss, IAAPiecewiseAffine, IAASharpen, MedianBlur,
                            MotionBlur, OneOf, OpticalDistortion, RandomBrightness, RandomContrast,
                            RandomRotate90, ShiftScaleRotate, Transpose, VerticalFlip,
                            )
from dlpipeline.augmentor.dlp_augmentor import DLPAugmentor

from dlpipeline.utilities.visualisation.bbox import visualize

__author__ = 'cnheider'


def strong_aug(p=.5):
  return Compose([
    RandomRotate90(),
    Flip(),
    Transpose(),
    OneOf([
      IAAAdditiveGaussianNoise(),
      GaussNoise(),
      ], p=0.2),
    OneOf([
      MotionBlur(p=.2),
      MedianBlur(blur_limit=3, p=.1),
      Blur(blur_limit=3, p=.1),
      ], p=0.2),
    ShiftScaleRotate(shift_limit=0.0625, scale_limit=0.2, rotate_limit=32, p=0.8),
    OneOf([
      OpticalDistortion(p=0.3),
      GridDistortion(p=.1),
      IAAPiecewiseAffine(p=0.3),
      ], p=0.2),
    OneOf([
      CLAHE(clip_limit=2),
      IAASharpen(),
      IAAEmboss(),
      RandomContrast(),
      RandomBrightness(),
      ], p=0.3),
    HueSaturationValue(p=0.3),
    ], p=p)


def get_bbox_aug(aug, min_area=0., min_visibility=0.):
  return Compose(aug, bbox_params={'format':        'coco',
                                   'min_area':      min_area,
                                   'min_visibility':min_visibility,
                                   'label_fields':  ['category_id']
                                   })


if __name__ == '__main__':

  import matplotlib.pyplot as plt
  from urllib.request import urlopen

  import numpy as np
  import cv2


  def augment_and_show(aug, image):
    image = aug(image=image)['image']
    plt.figure(figsize=(10, 10))
    plt.imshow(image)


  def download_image(url):
    data = urlopen(url).read()
    data = np.frombuffer(data, np.uint8)
    image = cv2.imdecode(data, cv2.IMREAD_COLOR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image


  augmentor = strong_aug(p=1)
  image = download_image(
      'https://d177hi9zlsijyy.cloudfront.net/wp-content/uploads/sites/2/2018/05/11202041/180511105900-atlas'
      '-boston-dynamics-robot-running-super-tease.jpg')
  augment_and_show(augmentor, image)
  plt.show()

  image = download_image('http://images.cocodataset.org/train2017/000000386298.jpg')

  annotations = {'image':      image,
                 'bboxes':     [[366.7, 80.84, 132.8, 181.84], [5.66, 138.95, 147.09, 164.88]],
                 'category_id':[18, 17]
                 }
  category_id_to_name = {17:'cat', 18:'dog'}

  visualize(annotations, category_id_to_name)
  plt.show()

  augmentor = get_bbox_aug([VerticalFlip(p=1)])
  augmented = augmentor(**annotations)
  visualize(augmented, category_id_to_name)


class AlbumentationsAugmentor(DLPAugmentor):
  pass