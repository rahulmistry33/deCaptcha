import os, cv2, string
from pathlib import Path
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
from keras import layers
from keras.models import Model
from keras.utils.vis_utils import plot_model
from keras.models import Sequential
from keras.layers import Dense
from keras.models import model_from_json
from django.conf import settings

# load json and create model
json_file = open('./crackCaptcha/WaterRipple_CNN_Model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)
# load weights into new model
model.load_weights("./crackCaptcha/WaterRipple_CNN_Model.h5")

model.compile(loss='categorical_crossentropy', optimizer='adam',metrics=["accuracy"])


symbols = string.ascii_lowercase + "0123456789"


def predict(filepath):
    img = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
    img = img / 255.0
    img = cv2.resize(img,(200,50))
    res = np.array(model.predict(img[np.newaxis, :, :, np.newaxis]))
    ans = np.reshape(res, (5, 36))
    captcha_chars = []
    for a in ans:
        captcha_chars.append(np.argmax(a))

    captcha = ''
    for c in captcha_chars:
        captcha += symbols[c]
        
    return captcha

def predict_waterripple_cnn(url_list):

    images = []
    preds = []
    
    for url in url_list:
        url = os.path.join(settings.MEDIA_ROOT,"images/"+url)
        preds.append(predict(url))

    return preds


