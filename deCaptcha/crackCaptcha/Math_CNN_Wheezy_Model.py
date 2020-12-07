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
json_file = open('./crackCaptcha/Math_CNN_Wheezy_Model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)
# load weights into new model
model.load_weights("./crackCaptcha/Math_CNN_Wheezy_Model.h5")
opt = optimizers.Adam(learning_rate=0.0001)

model.compile(loss='categorical_crossentropy', optimizer=opt,metrics=["accuracy"])

    
offset = 10
def getCodeReverse(i):
    if i == 10:
        return '+'
    if i == 11:
        return '-'
    return i

# images = []
# for i, img in enumerate(os.listdir('test_samples')):
#     im = Image.open(os.path.join('test_samples', img))
#     im = np.array(im) / 255.0
#     images.append(np.array(im))
    

# x_test = np.array(images)
# y_pred = model.predict_on_batch(x_test)
# y_pred = tf.math.argmax(y_pred, axis=-1)

# y_pred_modified = []
# for item in y_pred:
#   y_pred_modified.append("".join([str(getCodeReverse(i)) for i in item.numpy()]))

# for i, img in enumerate(os.listdir('test_samples')):
#     image = cv2.imread(os.path.join('test_samples', img))
#     plt.imshow(image)
#     plt.show()
#     print("Predicted Captcha = {}".format(y_pred_modified[i]))


def predict_math_cnn_wheezy(url_list):
    images = []
    for url in url_list:
        url = os.path.join(settings.MEDIA_ROOT,"images/"+url)
        im = Image.open(os.path.join(url))
        im = np.array(im) / 255.0
        images.append(np.array(im))

    x_test = np.array(images)
    y_pred = model.predict_on_batch(x_test)
    y_pred = tf.math.argmax(y_pred, axis=-1)
    y_pred_modified = []

    for item in y_pred:
        y_pred_modified.append("".join([str(getCodeReverse(i)) for i in item.numpy()]))

    return y_pred_modified







