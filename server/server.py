import os
import tensorflow as tf
from tensorflow import keras
from flask import Flask, flash, request, redirect, url_for
from flask_cors import CORS
from werkzeug.utils import secure_filename
from keras.models import load_model
from keras.preprocessing.image import img_to_array, ImageDataGenerator
from keras.applications import imagenet_utils
import PIL
from PIL import Image
from numpy import asarray

#import classifier
import numpy as np
import cv2
#import base64
#import json
import io
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

UPLOAD_FOLDER = '/Users/deathcat05/Desktop/ssu-geosciences-web/server/image'


models = '/Users/deathcat05/Desktop/ssu-geosciences-web/server/models'

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
           
@app.route('/')
def hello_world():
    return 'Backend up and running!'


@app.route('/classify', methods=['GET', 'POST'])
def classify():
    model = request.form['model']
    image = request.files['image']
    options = request.form['options']
    print('options are', options)
    
    image = Image.open(image)
    image = np.asarray(image.resize((224,224)))
    image = np.expand_dims(image, axis=0)
    

    '''
    image = request.files['file'].read()
    image = cv2.imdecode(np.frombuffer(image, dtype=np.uint8), -1)
    print(image)
    resized_image = cv2.resize(image, (224, 224))
    resized_image = np.reshape(resized_image, (224*224))

    #image = np.expand_dims(image, axis=0)
    print(resized_image)
    #image = cv2.resize(image, (224,224))
    #image = image.reshape()

    # preprocess the image and prepare it for classification
    #image = prepare_image(image, target=(224, 224))
    #print(resized_image)
'''
    if(model == 'resnet'):
        print('Model chosen is resnet')
        modelToUse = models +'/my_model_resnet50.h5'
        modelToUse =  keras.models.load_model(modelToUse)
        modelToUse.summary()
        #print(model)
        #prediction = model.predict(resized_image)
        #print(prediction)
    if(model == 'inception'):
        print('Model chosen is inception')
        modelToUse = models +'/my_model_inception_v3.h5'
        modelToUse =  keras.models.load_model(modelToUse)
        modelToUse.summary()

    if(model == 'vgg16'):
        print('Model chosen is vgg16')
        modelToUse = models +'/my_model_vgg16.h5'
        modelToUse =  keras.models.load_model(modelToUse)
        modelToUse.summary()

'''
@app.route('/classify', methods=['POST'])s
def classify():
    image = request.files['file'].read()
    option = request.form['options']
    print('option is:', option)
    image = cv2.imdecode(np.frombuffer(image, dtype=np.uint8), -1)
    resized_image = cv2.resize(image, (224, 224))
    #The NN Class instance
    NN = classifier.NN()
    NN.base_model = option
    load_base_model(option, None)
    labels = NN.clean_classify_one_image(resized_image)

    if (len(labels[0]) == 0):
        labels = ''
    print(labels)
    return str(labels).replace('"', "'")
'''

def prepare_image(image, target):
    # if the image mode is not RGB, convert it
    if image.mode != "RGB":
        image = image.convert("RGB")

    # resize the input image and preprocess it
    image = image.resize(target)
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image = imagenet_utils.preprocess_input(image)

    # return the processed image
    return image
if __name__ == '__main__':
    app.run()
