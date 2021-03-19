import numpy as np
import os
import PIL
import tensorflow as tf
import cv2

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
from keras.models import model_from_json
from django.conf import settings

batch_size = 32
img_height = 50
img_width = 200

num_classes = 6

type_names = {'Fishy':'FishEye', 'Mathematical':'Mathematical', 'Shadow':'Shadow', 'Sina4K':'Sina', 'WaterRipple':'WaterRipple', 'WheezyMath':'WheezyMath'}
class_names = ['Fishy', 'Mathematical', 'Shadow', 'Sina4K', 'WaterRipple', 'WheezyMath']
AUTOTUNE = tf.data.experimental.AUTOTUNE


# load json and create model
dir_path = os.path.dirname(os.path.realpath(__file__))
json_file = open(os.path.join(dir_path, 'classification.json'), 'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)
# load weights into new model
model.load_weights(os.path.join(dir_path, "classification.h5"))


model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

def get_captcha_type(url_list):
    type_list=[]
    for url in url_list:
        url = os.path.join(settings.MEDIA_ROOT,"images/"+url)
        img = keras.preprocessing.image.load_img(url, target_size=(img_height, img_width))
        img_array = keras.preprocessing.image.img_to_array(img)
        img_array = tf.expand_dims(img_array, 0) 

        predictions = model.predict(img_array)
        score = tf.nn.softmax(predictions[0])
        captcha_type = "{}".format(class_names[np.argmax(score)])
        type_list.append(type_names[captcha_type])
    return type_list
