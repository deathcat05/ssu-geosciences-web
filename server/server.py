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
import numpy as np
import cv2
from PIL import Image

#Allowed image extensions
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

#Image directory that will be used if directory is chosen
imagesDir = '/Users/deathcat05/Desktop/ssu-geosciences-web/server/images'

#Loading the base models 
models = '/Users/deathcat05/Desktop/ssu-geosciences-web/server/models'
inception_base_model = load_base_model("InceptionV3", (227, 227, 3))
resnet_base_model = load_base_model("ResNet50", (224, 224, 3))
vgg16_base_model = load_base_model("VGG16", (224, 224, 3))

app = Flask(__name__)
CORS(app)

#Grabbing file name from image
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
           
@app.route('/')
def start_app():
    return 'Backend up and running!'

@app.route('/classify', methods=['GET', 'POST'])
def classify():
    model = request.form['model']
    options = request.form['options']
    directory = request.form['directory']

    #This is only called if the user chose to classify one image
    if( 'image' in request.files):
        print('User wants to classify an image')
        image = request.files['image'].read()
        img = cv2.imdecode(np.frombuffer(image, dtype=np.uint8), -1)
        predict_one_image(img, model, options)

    #This will classify a directory of images for the user
    if(directory == 'directory'):
        print('User wants to classify a directory')
        new_image = load_images(imagesDir, 224)
        predict_images(new_image, model, options)

def load_images(folder, img_size):
        '''
        return an array containing all the images from the given folder.
        all images are converted to RGB in channel_last format, and resized
        to img_size x img_size
        '''

        images = []
        filenames = []
        ignore_list = ['.AppleDouble', 'pycache', '.DS_Store']
        for filename in os.listdir(folder):
                if filename in ignore_list:
                        continue
                img = Image.open(os.path.join(folder, filename))
                print(img)

                if img is not None:
                        rbgimg = Image.new("RGB", img.size)
                        rbgimg.paste(img)
                        rbgimg = rbgimg.resize((img_size, img_size), Image.ANTIALIAS)
                        np_img = np.array(rbgimg)
                        images.append(np_img)
                        filenames.append(filename)

        images = np.array(images)

        return images, filenames

def predict_one_image(imageToPredict, model, options):
    print('inside predict_one_image function')
    print('imageToPredict is: ', imageToPredict)
    print('options are:', options)

    if(model == 'inception'):
        print('Model chosen is inception')
        modelToUse = models +'/inceptionWeights.h5'
        print(modelToUse)

        #Resize image for inception model
        resized_image = cv2.resize(imageToPredict, (227, 227))
        resized_image = np.expand_dims(resized_image, axis=0)
        resized_image = resized_image / 255

        #Creating components for transfer learning prediction
        base_model = inception_base_model
        model = base_model[0]
        model_with_transfer = create_final_layers(model, 227, labels=['with', 'without'])
        print('print created final layers successful')
        model_with_transfer.load_weights(modelToUse)
        print('ran load_weights function')
        prediction = model_with_transfer.predict(resized_image)
        print(prediction)

        '''
       # prediction = model_with_transfer.predict(resized_image)
        predicted_classes = np.argmax(prediction, axis=1)
        prediction_list = prediction.tolist()
        withS = '{: .3f}'.format(prediction_list[0][0])
        withoutS = '{: .3f}'.format(prediction_list[0][1])
        predictions = withS + ',' + withoutS;
        print(predictions)
        return predictions
        '''
        return prediction
    
    if(model == 'resnet'):
        print('Model chosen is resnet')
        modelToUse = models +'/resnetWeights.h5'
        print(modelToUse)

        #Resize image for resnet model.
        resized_image = cv2.resize(imageToPredict, (224, 224))
        resized_image = np.expand_dims(resized_image, axis=0)
        resized_image = resized_image / 255

        #Creating components for transfer learning prediction
        base_model = resnet_base_model
        model = base_model[0]
        model_with_transfer = create_final_layers(model, 224, labels=['with', 'without'])
        print('print created final layers successful')
        model_with_transfer.load_weights(modelToUse)
        print('ran load_weights function')
        prediction = model_with_transfer.predict(resized_image)
        print(prediction)

        '''
       # prediction = model_with_transfer.predict(resized_image)
        predicted_classes = np.argmax(prediction, axis=1)
        prediction_list = prediction.tolist()
        withS = '{: .3f}'.format(prediction_list[0][0])
        withoutS = '{: .3f}'.format(prediction_list[0][1])
        predictions = withS + ',' + withoutS;
        print(predictions)
        return predictions
        '''
        return prediction
    
    if(model == 'vgg16'):
        print('Model chosen is vgg16')
        modelToUse = models +' /vgg16Weights.h5'

        #Resizing image for vgg model
        resized_image = cv2.resize(imageToPredict, (224, 224))
        resized_image = np.expand_dims(resized_image, axis=0)
        resized_image = resized_image / 255

        #Creating components for transfer learning prediction
        base_model = vgg16_base_model
        model = base_model[0]
        model_with_transfer = create_final_layers(model, 224, labels=['with', 'without'])
        print('print created final layers successful')
        model_with_transfer.load_weights(modelToUse)
        print('ran load_weights function')
        prediction = model_with_transfer.predict(resized_image)
        print(prediction)

        '''
       # prediction = model_with_transfer.predict(resized_image)
        predicted_classes = np.argmax(prediction, axis=1)
        prediction_list = prediction.tolist()
        withS = '{: .3f}'.format(prediction_list[0][0])
        withoutS = '{: .3f}'.format(prediction_list[0][1])
        predictions = withS + ',' + withoutS;
        print(predictions)
        return predictions
        '''
        return prediction

def predict_images(images, model, options):
    print('inside predict_images function')
    print('images are: ', images)
    print('model is:', model)
    print('options are:', options)
    if(model == 'inception'):
        print('Model chosen is inception')
        modelToUse = models +'/test.h5'
        print(modelToUse)
        base_model = inception_base_model
        model = base_model[0]
        model_with_transfer = create_final_layers(model, 227, labels=['with', 'without'])
        print('print created final layers successful')
        model_with_transfer.load_weights(modelToUse)
        prediction = model_with_transfer.predict(images)
        print(prediction)

        '''
       # prediction = model_with_transfer.predict(resized_image)
        predicted_classes = np.argmax(prediction, axis=1)
        prediction_list = prediction.tolist()
        withS = '{: .3f}'.format(prediction_list[0][0])
        withoutS = '{: .3f}'.format(prediction_list[0][1])
        predictions = withS + ',' + withoutS;
        print(predictions)
        return predictions
        '''
        return prediction

if __name__ == '__main__':
    app.run()
 
