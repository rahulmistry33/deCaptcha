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


# load json and create model
print("Halo ji")
json_file = open('WaterRipple_CNN_Model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
print("Loaded JSON")
model = model_from_json(loaded_model_json)
# load weights into new model
model.load_weights("WaterRipple_CNN_Model.h5")
print("Loaded model from disk")

model.compile(loss='categorical_crossentropy', optimizer='adam',metrics=["accuracy"])


symbols = string.ascii_lowercase + "0123456789"


def predict(filepath):
    img = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
    if img is not None:
        img = img / 255.0
    else:
        print("Not detected")
    res = np.array(model.predict(img[np.newaxis, :, :, np.newaxis]))
    ans = np.reshape(res, (5, 36))
    captcha_chars = []
    for a in ans:
        captcha_chars.append(np.argmax(a))

    captcha = ''
    for c in captcha_chars:
        captcha += symbols[c]
        
    return captcha


for i, img in enumerate(os.listdir('test_samples')):
    #Read image as grayscale
    image = cv2.imread(os.path.join('test_samples', img))
    plt.imshow(image)
    plt.show()
    predicted=predict(os.path.join('test_samples',img))
    print("Predicted Captcha =",predicted)


