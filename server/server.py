import os
import tensorflow as tf
from tensorflow import keras
from flask import Flask, flash, request, redirect, url_for
from flask_cors import CORS
from werkzeug.utils import secure_filename
from keras.models import Model, load_model#, load_weights
from keras.preprocessing import image#, img_to_array
from numpy import asarray

from keras.applications.inception_v3 import decode_predictions
from keras.applications.inception_v3 import preprocess_input as inception_v3_preprocess_input

from model import load_base_model, create_final_layers

#import classifier
import numpy as np
import cv2
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

UPLOAD_FOLDER = '/Users/deathcat05/Desktop/ssu-geosciences-web/server/image'

#Loading the base models 
models = '/Users/deathcat05/Desktop/ssu-geosciences-web/server/models'
inception_base_model = load_base_model("InceptionV3", (227, 227, 3))
resnet_base_model = load_base_model("ResNet50", (224, 224, 3))
vgg16_base_model = load_base_model("VGG16", (224, 224, 3))

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
           
@app.route('/')
def start_app():
    return 'Backend up and running!'

@app.route('/classify', methods=['GET', 'POST'])
def classify():
    model = request.form['model']
    image = request.files['image'].read()
    options = request.form['options']
    print('options are', options)

    img = cv2.imdecode(np.frombuffer(image, dtype=np.uint8), -1)
    resized_image = cv2.resize(img, (227, 227))
    resized_image = np.expand_dims(resized_image, axis=0)
    resized_image = resized_image / 255 


    if(model == 'resnet'):
        print('Model chosen is resnet')

        modelToUse = models + '/test.h5'
        base_model = resnet_base_model
        model = base_model[0]
        model_with_transfer = create_final_layers(model, 224, labels=['with', 'without'])
        model_with_transfer.load_weights(modelToUse)
        prediction = model_with_transfer.predict(resized_image)
        predicted_classes = np.argmax(prediction, axis=1)
        print(prediction)
        print(predicted_classes)
        return predicted_classes



    if(model == 'inception'):
        print('Model chosen is inception')
       
        modelToUse = models +'/test.h5'
        base_model = inception_base_model
        model = base_model[0]
        model_with_transfer = create_final_layers(model, 227, labels=['with', 'without'])
        model_with_transfer.load_weights(modelToUse)
        prediction = model_with_transfer.predict(resized_image)
        predicted_classes = np.argmax(prediction, axis=1)
        prediction_list = prediction.tolist()
        prediction_string = str(prediction_list).split(',')
        prediction_string[0].replace('[', '')
        prediction_string[1].replace(']', '')
        print(prediction_string[0])
        print(prediction_string[1])

        if(predicted_classes == 0):
            return ('with sigma:' + prediction_string[0] + '%')
        if(predicted_classes == 1): 
            return ('without sigma:' + prediction_string[1] + '%')
        

    if(model == 'vgg16'):
        print('Model chosen is vgg16')
        modelToUse = models + '/test.h5'
        base_model = vgg16_base_model
        model = base_model[0]
        model_with_transfer = create_final_layers(
            model, 227, labels=['with', 'without'])
        model_with_transfer.load_weights(modelToUse)
        prediction = model_with_transfer.predict(resized_image)
        predicted_classes = np.argmax(prediction, axis=1)
        prediction_list = prediction.tolist()
        print(prediction_list)
        print(predicted_classes)

        if(predicted_classes == 0):
            return 'with sigma: '
        if(predicted_classes == 1):
            return 'without sigma'

if __name__ == '__main__':
    app.run()
 