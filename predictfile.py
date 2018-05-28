import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
from keras.models import Sequential, load_model
import keras, sys
import numpy as np
from PIL import Image

classes = ["clean", "messy"]
num_classes = len(classes)
image_size = 50

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('There is no file')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('There is no file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filepath =  os.path.join(app.config['UPLOAD_FOLDER'], filename)

            model = load_model('./cnn.h5')

            image = Image.open(filepath)
            image = image.convert('RGB')
            image = image.resize((image_size, image_size))
            data = np.asarray(image)
            X = []
            X.append(data)
            X = np.array(X)

            result = model.predict([X])[0]
            predicted = result.argmax()

            percentage = int(result[predicted] * 100)

            return "Your room is: " + classes[predicted] + ", percentage: " + str(percentage) + "%"

    return '''
    <!doctype html>
    <html>
    <head>
    <link rel= "stylesheet" type= "text/css" href= "../styles/mainpage.css">
    <title>Upload your room pic, and invite the girl to your room</title></head>
    <body>
    <h1>Upload your room pic, and invite the girl to your room</h1>
    <form method = post enctype = multipart/form-data>
    <p><input type=file name=file>
    <input type=submit value=Upload>
    </form>
    </body>
    </html>
    '''

from flask import send_from_directory

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
