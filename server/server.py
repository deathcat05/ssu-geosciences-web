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
#Needed for confusion matrix
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import itertools  


#Allowed image extensions
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

#Image directory that will be used if directory is chosen
imagesDir = '/Users/deathcat05/Desktop/ssu-geosciences-web/server/images/'

#Loading the base models 
models = '/Users/deathcat05/Desktop/ssu-geosciences-web/server/models'
inception_base_model = load_base_model("InceptionV3", (227, 227, 3))
#resnet_base_model = load_base_model("ResNet50", (224, 224, 3))
#vgg16_base_model = load_base_model("VGG16", (224, 224, 3))

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
        return predict_one_image(img, model, options)

    #This will classify a directory of images for the user
    if(directory == 'directory'):
        print('User wants to classify a directory')
        new_image = load_images(imagesDir, 227)
        return predict_images(new_image, model, options)

def load_images(folder, img_size):
        '''
        return an array containing all the images from the given folder.
        all images are converted to RGB in channel_last format, and resized
        to img_size x img_size
        '''

        images = []
        #filenames = []
        ignore_list = ['.AppleDouble', '__pycache__', '.DS_Store']
        for filename in os.listdir(folder):
                if(filename in ignore_list):
                        continue

                img = Image.open(os.path.join(folder, filename))
                if img is not None:
                        rgb_image = Image.new("RGB", img.size)
                        rgb_image.paste(img)
                        rgb_image = rgb_image.resize((img_size, img_size), Image.ANTIALIAS)
                        image_as_array = np.array(rgb_image)
                        images.append(image_as_array)

        images = np.array(images)
        return images

def predict_one_image(imageToPredict, model, options):
    print('inside predict_one_image function')
    print('options are:', options)

    if(model == 'inception'):
        print('Model chosen is inception')
        modelToUse = models + '/test.h5'
        #modelToUse = models + '/inceptionWeights.h5'
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
        print('Prediction is:', prediction)

        #Need to convert the array to indvidual strings so that the data can be cleanly sent back to front-end
        prediction_list = prediction.tolist()
        withS = '{: .3f}'.format(prediction_list[0][0])
        withS_string = "With Sigma:" + withS
        withoutS = '{: .3f}'.format(prediction_list[0][1])
        withoutS_string = "Without Sigma:" + withoutS
        predictions = withS_string + ',' + withoutS_string
        print(predictions)
        return predictions
        
        #return prediction
    
    if(model == 'resnet'):
        print('Model chosen is resnet')
        #modelToUse = models + '/resnetWeights.h5'
        modelToUse = models + '/test.h5'
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

        #Need to convert the array to a list so that the data can be cleanly sent back to front-end
        print('Prediction is:', prediction)
        prediction_list = prediction.tolist()
        withS = '{: .3f}'.format(prediction_list[0][0])
        withoutS = '{: .3f}'.format(prediction_list[0][1])
        predictions = withS + ',' + withoutS
        print(predictions)
        return predictions
        #return prediction
    
    if(model == 'vgg16'):
        print('Model chosen is vgg16')
        modelToUse = models + '/vgg16Weights.h5'

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
        print('Prediction is:, ', prediction)

        
       #Need to convert the array to a string so that the data can be cleanly sent back to front-end
        prediction_list = prediction.tolist()
        withS = '{: .3f}'.format(prediction_list[0][0])
        withS_string = "With Sigma:" + withS
        print(withS_string)
        withoutS = "Without Signma: " + '{: .3f}'.format(prediction_list[0][1])
        predictions = withS + ',' + withoutS
        print(predictions)
        return predictions

def predict_images(images, model, options):
    print('inside predict_images function')
    predictions = []
    actual = [1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0]
    if(model == 'inception'):
        print('Model chosen is inception')
        modelToUse = models +'/test.h5'
        base_model = inception_base_model
        model = base_model[0]
        model_with_transfer = create_final_layers(model, 227, labels=['with', 'without'])
        print('print created final layers successful')
        model_with_transfer.load_weights(modelToUse)
        print('load_weights successful')
        total_images = len(images)
        print(total_images)
        for image in images:
                resized_image = np.expand_dims(image, axis=0)
                prediction = model_with_transfer.predict(resized_image)
                predicted_class = np.argmax(prediction)
                predictions.append(predicted_class)
                #predicted_class = predicted_class / total_images
        print(predictions)

        #For Confusion matrix
        '''
        conf_matrix = confusion_matrix(actual, predictions)
        conf_matrix = conf_matrix.astype('float') / conf_matrix.sum(axis=1)[:, np.newaxis]
        row1 = np.array2string(conf_matrix[0])
        row2 = np.array2string(conf_matrix[1])
        conf_matrix_as_string = row1 + ',' + row2
        return conf_matrix_as_string
        '''
        classes = [0, 1]
        title = "Confusion matrix"
        conf_matrix = confusion_matrix(actual, predictions, labels=[0, 1])
        conf_matrix = conf_matrix.astype('float') / conf_matrix.sum(axis=1)[:, np.newaxis]
        #cmap = plt.conf_matrix.Blues
        plt.figure()
        plt.imshow(conf_matrix, interpolation='nearest', cmap=plt.cm.Blues)
        plt.title(title)
        plt.colorbar()
        tick_marks = np.arange(len(classes))
        plt.xticks(tick_marks, classes, rotation=45)
        plt.yticks(tick_marks, classes)
        fmt = '.2f'
        thresh = conf_matrix.max() / 2.
        for i, j in itertools.product(range(conf_matrix.shape[0]), range(conf_matrix.shape[1])):
                plt.text(j, i, format(conf_matrix[i, j], fmt), horizontalalignment="center", color="white" if conf_matrix[i, j] > thresh else "black")

        plt.ylabel('True label')
        plt.xlabel('Predicted label')
        plt.tight_layout()
        plt.savefig('confusion_matrix.jpg')
        
if __name__ == '__main__':
    app.run()
 