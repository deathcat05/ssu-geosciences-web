import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

import classifier
import numpy as np
import cv2
import base64
import json
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


UPLOAD_FOLDER = '/Users/deathcat05/Desktop/ssu-preserves-web/server/image'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#The NN Class instance 
NN = classifier.NN()

@app.route('/')
def hello_world():
        return 'Backend up and running!'


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            # print(UPLOAD_FOLDER)
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)) 
            classify_image(file)
            return 'file uploaded successfully!'

def classify_image(file):
    print('in classify_image function')
    image = file.read()
    image = cv2.imdecode(np.fromstring(image, dtype=np.uint8), -1)
    resized_image = cv2.resize(image, (224,224))
    labels = NN.clean_classify_one_image(resized_image, lang)
    if (len(labels[0]) == 0):
        labels = ''
    print(labels)
    return str(labels).replace('"',"'")

if __name__ == '__main__':
    app.run()

