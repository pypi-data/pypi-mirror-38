from keras.layers.convolutional import _Conv
from keras.layers.pooling import _Pooling2D

import numpy as np

import cv2

def get_last_visualization_layer(model):
    for index in range(0, len(model.layers)):
        layer = model.layers[-index]
        if isinstance(layer, _Conv) or isinstance(layer, _Pooling2D):
            return layer
    return None

def prepare_image(image, size):
    image = cv2.resize(image, size)
    return np.reshape(image, (1, *size, 3))