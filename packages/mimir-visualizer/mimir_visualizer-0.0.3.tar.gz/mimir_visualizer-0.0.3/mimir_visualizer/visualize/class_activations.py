from keras.layers import Activation, GlobalAveragePooling2D

from .utils import get_last_visualization_layer, prepare_image

import keras.backend as K
import numpy as np

import cv2

def _gradcam_visualization(model, input_image, class_index=None, 
    layer_index=None, layer_name=None):
    """
        Creates a class actiation map using the gradient weighted 
        class activation map approach. Based on paper by Selvaraju et al.

        # Source 
            https://arxiv.org/abs/1610.02391
    """

    input_layer = model.layers[0].input
    output_layer = model.layers[-1].output
    target_layer = model.get_layer(layer_name, layer_index).output

    number_of_classes = int(output_layer.shape[1])

    loss = K.sum(output_layer * K.one_hot([class_index], number_of_classes))

    gradients = K.gradients(loss, target_layer)[0]
    gradients /= (K.sqrt(K.mean(K.square(gradients))) + K.epsilon())

    weights = GlobalAveragePooling2D()(gradients)

    gradcam = K.sum(weights * target_layer, axis=-1)
    gradcam = Activation('relu')(gradcam)

    gradcam_fn = K.function([input_layer], [gradcam])

    gradcam = gradcam_fn([input_image])
    gradcam = cv2.resize(np.squeeze(gradcam), tuple(input_layer.shape[1:3]))

    return gradcam / np.max(gradcam)

def _deprocess_cam(image, cam):
    """
        Converts class activation map to viewable image and
        applies heatmap filter.
    """
    
    if np.ndim(image) > 3:
        image = np.squeeze(image)

    image -= np.min(image)     
    image  = np.minimum(image, 255)

    cam = cv2.applyColorMap(np.uint8(255 * cam), cv2.COLORMAP_JET)
    cam = np.float32(cam) + np.float32(image)
    cam = 255 * cam / np.max(cam)

    # cam = cv2.cvtColor(cam, cv2.COLOR_BGR2RGB)

    return cam

def generate_gradcam(model, input_image, class_index=None, 
    layer_index=None, layer_name=None, image_modifiers=None):
    """
        Helper function to generate gradcam.
    """

    K.set_learning_phase(0)

    input_size = tuple(model.input.shape[1:3])

    input_image = prepare_image(input_image, input_size)
    source_image = input_image

    if layer_index is None and layer_name is None:
        layer_name = get_last_visualization_layer(model).name

    if image_modifiers is not None:
        input_image = image_modifiers(input_image)

    gradcam = _gradcam_visualization(model, input_image.astype(np.float32),
        class_index, layer_index, layer_name)

    return  _deprocess_cam(source_image, gradcam)