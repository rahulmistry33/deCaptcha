import os, cv2, string
from pathlib import Path
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
from keras import layers, optimizers
from keras.models import Model
from keras.utils.vis_utils import plot_model
from keras.models import Sequential
from keras.layers import Dense
from keras.models import model_from_json
from PIL import Image
import tensorflow as tf
from django.conf import settings

# load json and create model
json_file = open('./crackCaptcha/Sina_CNN_Model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)
# load weights into new model
model.load_weights("./crackCaptcha/Sina_CNN_Model.h5")
opt = optimizers.Adam(learning_rate=0.0001)

model.compile(loss='categorical_crossentropy', optimizer=opt,metrics=["accuracy"])

    
offset = 10
def getCodeReverse(i):
  if i >= 10:
    return chr(i + 65 - offset)
  return i

def predict_sina_cnn(url_list):
    images = []
    y_pred_modified = []
    
    for url in url_list:
      url = os.path.join(settings.MEDIA_ROOT,"images/"+url)

      # im = Image.open(url)
      img = cv2.imread(url)
      img = img / 255.0
      img = cv2.resize(img,(420,45))
      # im = np.array(im) / 255.0
      images.append(np.array(img))

    x_test = np.array(images)
    y_pred = model.predict_on_batch(x_test)
    y_pred = tf.math.argmax(y_pred, axis=-1)

    for item in y_pred:
      y_pred_modified.append("".join([str(getCodeReverse(i)) for i in item.numpy()]))

    return y_pred_modified
  

    






