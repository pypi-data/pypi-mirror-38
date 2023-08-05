import json
import pickle as pk

import numpy as np
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.preprocessing.image import img_to_array, load_img
# Load models and support
from tensorflow.python.keras.applications.imagenet_utils import preprocess_input
from tensorflow.python.keras.utils import get_file


with open('models/vgg16_cat_list.pk', 'rb') as f:
  cat_list = pk.load(f)

CLASS_INDEX = None
CLASS_INDEX_PATH = 'https://s3.amazonaws.com/deep-learning-models/image-models/imagenet_class_index.json'
#CLASS_INDEX_PATH = 'imagenet_class_index.json'

def get_predictions(predictions, top=5):
  global CLASS_INDEX
  if len(predictions.shape) != 2 or predictions.shape[1] != 1000:
    raise ValueError(
        f'`decode_predictions` expects a batch of predictions (i.e. a 2D array of shape (samples, '
        f'1000)). Found array with shape: {str(predictions.shape)}')
  if CLASS_INDEX is None:
    file_path = get_file('imagenet_class_index.json',
                     CLASS_INDEX_PATH,
                     cache_subdir='models')
    CLASS_INDEX = json.load(open(file_path))
  l = []
  for prediction in predictions:
    top_indices = prediction.argsort()[-top:][::-1]
    indexes = [tuple(CLASS_INDEX[str(i)]) + (prediction[i],) for i in top_indices]
    indexes.sort(key=lambda x:x[2], reverse=True)
    l.append(indexes)
  return l


def prepare_img_224(img_path):
  img = load_img(img_path, target_size=(224, 224))
  x = img_to_array(img)
  x = np.expand_dims(x, axis=0)
  x = preprocess_input(x)
  return x


def get_predicted_categories(img_224, model)-> list:
  out = model.predict(img_224)
  topn = get_predictions(out, top=5)
  return topn


def prepare_img_256(img_path):
  img = load_img(img_path, target_size=(256, 256))  # this is a PIL image
  x = img_to_array(img)  # this is a Numpy array with shape (3, 256, 256)
  x = x.reshape((1,) + x.shape) / 255
  return x


def car_damage_gate(img_256, model):
  print("Validating that damage exists...")
  pred = model.predict(img_256)
  if pred[0][0] <= .5:
    return True  # print("Validation complete - proceed to location and severity determination")
  else:
    return False
  # print("Are you sure that your car is damaged? Please submit another picture of the damage.")
  # print("Hint: Try zooming in/out, using a different angle or different lighting")


def location_assessment(img_256, model):
  print("Determining location of damage...")
  pred = model.predict(img_256)
  pred_label = np.argmax(pred, axis=1)
  d = {0:'Front', 1:'Rear', 2:'Side'}
  for key in d.keys():
    if pred_label[0] == key:
      return d[key]



def severity_assessment(img_256, model):
  print("Determining severity of damage...")
  pred = model.predict(img_256)
  pred_label = np.argmax(pred, axis=1)
  d = {0:'Minor', 1:'Moderate', 2:'Severe'}
  for key in d.keys():
    if pred_label[0] == key:
      return d[key]


# load models
def engine(img_path):
  image_net_model = VGG16(weights='imagenet')
  img_224 = prepare_img_224(img_path)
  top_n_prediction = get_predicted_categories(img_224, image_net_model)



  classier = load_model('static/models/d3_ft_model.h5')
  img_256 = prepare_img_256(img_path)
  category_result = classier(img_256)
  x = 0
  y = 0

  zipped = [a for a in zip(*top_n_prediction[0])]

  result = {'gate1':        'Categories',
            'gate1_result': ''.join([f'{cat}: {prob},\n\n' for cat,prob in zip(zipped[1],
                                                                               zipped[2])]),
            'gate2':        'Presence check: ',
            'gate2_result': 1,
            'gate2_message': {0:None, 1:None},
            'location':     x,
            'severity':     y,
            'final':        'Assessment complete!'
            }
  return result
