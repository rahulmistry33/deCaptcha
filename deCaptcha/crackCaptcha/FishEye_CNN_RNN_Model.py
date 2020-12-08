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
import keras
from django.conf import settings


class CTCLayer(layers.Layer):
    def __init__(self, name=None,**kwargs):
        super().__init__(name=name)
        self.loss_fn = keras.backend.ctc_batch_cost

    def call(self, y_true, y_pred):
        # Compute the training-time loss value and add it
        # to the layer using `self.add_loss()`.
        batch_len = tf.cast(tf.shape(y_true)[0], dtype="int64")
        input_length = tf.cast(tf.shape(y_pred)[1], dtype="int64")
        label_length = tf.cast(tf.shape(y_true)[1], dtype="int64")

        input_length = input_length * tf.ones(shape=(batch_len, 1), dtype="int64")
        label_length = label_length * tf.ones(shape=(batch_len, 1), dtype="int64")

        loss = self.loss_fn(y_true, y_pred, input_length, label_length)
        self.add_loss(loss)

        # At test time, just return the computed predictions
        return y_pred



# load json and create model
json_file = open('./crackCaptcha/FishEye_CNN_RNN_Model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json,custom_objects={'CTCLayer': CTCLayer})
# load weights into new model
model.load_weights("./crackCaptcha/FishEye_CNN_RNN_Model.h5")
opt = optimizers.Adam()

model.compile(optimizer=opt)
max_length = 5
downsample_factor = 4


characters = ['5', 'e', '6', 'f', 'w', 'b', 'r', '3', 'x', '2', 'p', '4', 'y', '7', 'd', 'n', 'm', 'k', 'c', '8', 'g', 'a', 'h']

# Mapping characters to integers
char_to_num = layers.experimental.preprocessing.StringLookup(
    vocabulary=list(characters), num_oov_indices=0, mask_token=None
)

# Mapping integers back to original characters
num_to_char = layers.experimental.preprocessing.StringLookup(
    vocabulary=char_to_num.get_vocabulary(), mask_token=None, invert=True
)


def decode_batch_predictions(pred):
    input_len = np.ones(pred.shape[0]) * pred.shape[1]
    # Use greedy search. For complex tasks, you can use beam search
    results = keras.backend.ctc_decode(pred, input_length=input_len, greedy=True)[0][0][
        :, :max_length
    ]
    # Iterate over the results and get back the text
    output_text = []
    for res in results:
        res = tf.strings.reduce_join(num_to_char(res)).numpy().decode("utf-8")
        output_text.append(res)
    return output_text


img_width = 200
img_height = 50

def predict_fisheye_cnn_rnn(url_list):
    images = []
    for url in url_list:
        url = os.path.join(settings.MEDIA_ROOT,"images/"+url)
        img = tf.io.read_file(url)
        img = tf.io.decode_png(img, channels=1)
        img = tf.image.convert_image_dtype(img, tf.float32)
        # print(img.shape)
        img = tf.image.resize(img, [img_height, img_width])
        # print(img.shape)
        img = tf.transpose(img, perm=[1, 0, 2])
        images.append(np.array(img))

    x_test = np.array(images)
    prediction_model2 = keras.models.Model(
        model.get_layer(name="image").input, model.get_layer(name="dense2").output
    )
    preds = prediction_model2.predict(x_test)

    return decode_batch_predictions(preds)
    
