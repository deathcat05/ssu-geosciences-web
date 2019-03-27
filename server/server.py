import os
from flask import Flask, flash, request, redirect, url_for
from flask_cors import CORS
from werkzeug.utils import secure_filename

import classifier
import numpy as np
import cv2
import base64
import json
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

UPLOAD_FOLDER = '/Users/deathcat05/Desktop/ssu-preserves-web/server/image'
app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


#The NN Class instance
NN = classifier.NN()

@app.route('/')
def hello_world():
    return 'Backend up and running!'


@app.route('/classify', methods=['POST'])
def classify():
    image = request.files['file'].read()
    image = cv2.imdecode(np.frombuffer(image, dtype=np.uint8), -1)
    resized_image = cv2.resize(image, (224, 224))
    labels = NN.clean_classify_one_image(resized_image)
    if (len(labels[0]) == 0):
        labels = ''
    print(labels)
    return str(labels).replace('"', "'")

if __name__ == '__main__':
    app.run()
