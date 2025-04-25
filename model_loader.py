

import tensorflow as tf

# Load the saved VGG-19 model
def get_model():
    return tf.keras.models.load_model("C:\\MajorProject8thsem\\emotion_vgg19.h5")
