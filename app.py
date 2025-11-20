from flask import Flask, render_template, request
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
import os

app = Flask(__name__)

# Load the trained model
model = load_model('healthy_vs_rotten.h5')

# Full list of class labels (28)
class_names = [
    'Apple___Healthy', 'Apple___Rotten',
    'Banana___Healthy', 'Banana___Rotten',
    'Bellpepper___Healthy', 'Bellpepper___Rotten',
    'Carrot___Healthy', 'Carrot___Rotten',
    'Cucumber___Healthy', 'Cucumber___Rotten',
    'Grape___Healthy', 'Grape___Rotten',
    'Guava___Healthy', 'Guava___Rotten',
    'Jujube___Healthy', 'Jujube___Rotten',
    'Mango___Healthy', 'Mango___Rotten',
    'Orange___Healthy', 'Orange___Rotten',
    'Pomegranate___Healthy', 'Pomegranate___Rotten',
    'Potato___Healthy', 'Potato___Rotten',
    'Strawberry___Healthy', 'Strawberry___Rotten',
    'Tomato___Healthy', 'Tomato___Rotten'
]

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    file = request.files['file']

    if not allowed_file(file.filename):
        return render_template('index.html', prediction="Only .png, .jpg, .jpeg files are allowed.")

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # Cleanup old files (keep last 5)
    uploaded_files = sorted(
        [os.path.join(UPLOAD_FOLDER, f) for f in os.listdir(UPLOAD_FOLDER)],
        key=os.path.getctime
    )
    if len(uploaded_files) > 5:
        for f in uploaded_files[:-5]:
            os.remove(f)

    # Preprocess image
    img = load_img(file_path, target_size=(150, 150))
    img_array = img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    # Predict
    prediction = model.predict(img_array)
    pred_index = np.argmax(prediction)
    confidence = float(np.max(prediction)) * 100
    label = f"{class_names[pred_index]} ({confidence:.2f}%)"

    return render_template('index.html', prediction=label, image=file.filename)

if __name__ == '__main__':
    app.run(debug=True)
