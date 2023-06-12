from __future__ import division, print_function
from werkzeug.utils import secure_filename
import sys
print(sys.executable)

import os
import glob
import re
import numpy as np

# Keras
from tensorflow.keras.applications.imagenet_utils import preprocess_input, decode_predictions
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.optimizers import Adam

# Flask
from flask import Flask, redirect, url_for, request, render_template

# Waitress
from waitress import serve

# Define a flask app
app = Flask(__name__, template_folder='templates', static_folder='static')

# Load your trained model
model = load_model("LatestModel.h5", compile=False)
model.make_predict_function()        # Necessary

print('Model loaded. Check http://127.0.0.1:5000/')

def model_predict(img_path, model):
    img = image.load_img(img_path, target_size=(224, 224))

    # Preprocessing the image
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)

    # Be careful how your trained model deals with the input
    # otherwise, it won't make correct prediction!
    x = preprocess_input(x, mode='caffe')

    preds = model.predict(x)
    return preds

@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')

class_mapping = {
    0: "Common Rust",
    1: "Healthy",
    2: "Gray Leaf Spot",
    3: "Northern Corn Leaf Blight",
    4: "Phaeosphaeria Leaf Spot",
    5: "Southern Rust"
}

def is_leaf(preds):
    # Define a threshold for classification confidence
    threshold = 0.5

    # Check if the highest predicted probability is above the threshold
    if np.max(preds) > threshold:
        return True
    else:
        return False

@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']
        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        upload_dir = os.path.join(basepath, 'uploads')
        os.makedirs(upload_dir, exist_ok=True)  # Create directory if it does not exist
        file_path = os.path.join(upload_dir, secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        preds = model_predict(file_path, model)

        # Check if the image is a leaf
        if is_leaf(preds):
            # Process your result for human
            pred_class_index = np.argmax(preds)
            pred_class = class_mapping[pred_class_index]
            return pred_class
        else:
            return "This is not a leaf."

    return None

if __name__ == '__main__':
   # Debug/Development
   # app.run(debug=True,host="0.0.0.0",port="5000")

   # Production
   serve(app, host='0.0.0.0', port=5000)