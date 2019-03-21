import os
import os.path
from PIL import Image

import numpy as np
import keras 

from keras.applications.inception_v3 import decode_predictions
from keras.applications.inception_v3 import preprocess_input as inception_v3_preprocess_input
import tensorflow as tf


class NN(object):
    def __init__(self):
        self.base_model = load_base_model('ResNet50', None)
        self.graph = tf.get_default_graph()

        # Use correct image preprocessing for model
        if self.base_model.name == ('inception_v3'):
            preprocess_input = inception_v3_preprocess_input
        else:
            preprocess_input = preprocess_input_wrapper
        self.kill = False

    def run(self):
        # Rewrite this bad boy
        waitForIn = threading.Thread(target=self.waitForTerminate)
        waitForIn.start()
        while True:
           # images, filenames = load_images('image', 224)
            if len(filenames) == 0:
                if self.kill:
                    print("The user terminated the program\n")
                    exit(0)
                time.sleep(2)
            else:
                if self.kill:
                    print("The user terminated the program\n")
                    exit(0)
                print("predicted: ")
                print(self.clean_classify_one_image(self, image))
    
    def clean_classify_one_image(self, image):
        # img shape needed: (224,224,3)
        # rbgimg = rbgimg.resize((img_size, img_size), Image.ANTIALIAS)
        image = np.expand_dims(image, axis=0)
        with self.graph.as_default():
            preds = self.base_model.predict(image)
            preds = decode_predictions(preds, top=10)[0]
        names = []
        for i in range(len(preds)):
            if preds[i][2]>0.1:
                names.append(preds[i][1])
            else:
                break
        return names

    def waitForTerminate(self):
        terminate = input()
        self.kill = True
        exit(0)

def load_base_model(model_name, input_shape=None):
    if model_name == 'InceptionV3':
        if input_shape == None:
            img_size = 227
            input_shape = (img_size, img_size, 3)
        base_model = keras.applications.inception_v3.InceptionV3(weights='imagenet',
                                                                 include_top = True,
                                                                 input_shape=input_shape,
                                                                 pooling = 'avg')
    elif model_name == 'ResNet50':
        if input_shape == None:
            img_size = 224
            input_shape = (img_size, img_size, 3)
        base_model = keras.applications.resnet50.ResNet50(weights='imagenet',
                                                          include_top = True,
                                                          input_shape = input_shape,
                                                          pooling = 'avg')
    return base_model

def preprocess_input_wrapper(x):
    """Wrapper around keras.applications.imagenet_utils.preprocess_input()
    to make it compatible for use with keras.preprocessing.image.ImageDataGenerator's
    `preprocessing_function` argument.
    Parameters
    ----------
    x : a numpy 3darray (a single image to be preprocessed)
    Note we cannot pass keras.applications.imagenet_utils.preprocess_input()
    directly to to keras.preprocessing.image.ImageDataGenerator's
    `preprocessing_function` argument because the former expects a
    4D tensor whereas the latter expects a 3D tensor. Hence the
    existence of this wrapper.
    Returns a numpy 3darray (the preprocessed image).
    """

    X = np.expand_dims(x, axis=0)
    X = imagenet_utils_preprocess_input(X)
    return X[0]

if __name__ == "__main__":
    classifier = NN()
    classifier.run()
