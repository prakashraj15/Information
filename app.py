
from classification import CustomNet, transform
from extract import on_prediction
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
import torch
import cv2
from roboflow import Roboflow
from PIL import Image

load_dotenv()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

app = Flask(__name__)


model = CustomNet(num_classes=3).to(device)

loaded_state_dict = torch.load(
    os.getenv('MODEL_PATH'),  map_location=device)
model.load_state_dict(loaded_state_dict)

model.eval()

rfAadhaar = Roboflow(api_key=str(os.getenv('AADHAAR_API_KEY')))
projectAadhar = rfAadhaar.workspace().project(
    str(os.getenv('AADHAAR_PROJECT_NAME')))
modelAadhar = projectAadhar.version(4).model

rfPan = Roboflow(api_key=str(os.getenv('PAN_API_KEY')))
projectPan = rfPan.workspace().project(str(os.getenv('PAN_PROJECT_NAME')))
modelPan = projectPan.version(1).model

rfPassport = Roboflow(api_key=str(os.getenv('PASSPORT_API_KEY')))
projectPassport = rfPassport.workspace().project(
    str(os.getenv('PASSPORT_PROJECT_NAME')))
modelPassport = projectPassport.version(1).model


@app.route('/')
def index():
    try:
        return render_template('test.html')
    except Exception as e:
        return render_template('test.html')


@app.route('/classify', methods=['POST'])
def classify_image():
    try:
        file = request.files['file']
        file_path = os.path.join(os.getenv('UPLOAD_PATH'), file.filename)
        file.save(file_path)
        img = Image.open(file_path)
        img = transform(img)
        img = img.unsqueeze(0)
        img = img.to(device)

        with torch.no_grad():
            output = model(img)

        predicted_class = torch.argmax(output).item()

        if (predicted_class == 0):
            return redirect(url_for('aadhaar', filename=file.filename))
        elif (predicted_class == 1):
            return redirect(url_for('pan', filename=file.filename))
        else:
            return redirect(url_for('passport', filename=file.filename))

    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500


@app.route('/pan/<filename>')
def pan(filename):
    path = os.path.join(os.getenv('UPLOAD_PATH'), filename)
    try:
        prediction = modelPan.predict(
            path, confidence=5, overlap=30).json()
        data = on_prediction(prediction, cv2.imread(path))
        data['type'] = 'pan'
        return jsonify(data), 200
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500


@app.route('/aadhaar/<filename>')
def aadhaar(filename):
    path = os.path.join(os.getenv('UPLOAD_PATH'), filename)
    try:
        prediction = modelAadhar.predict(
            path, confidence=5, overlap=30).json()
        data = on_prediction(prediction, cv2.imread(path))
        data['type'] = 'aadhaar'
        return jsonify(data), 200
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500


@app.route('/passport/<filename>')
def passport(filename):
    path = os.path.join(os.getenv('UPLOAD_PATH'), filename)
    try:
        prediction = modelPassport.predict(
            path, confidence=5, overlap=30).json()
        data = on_prediction(prediction, cv2.imread(path))
        data['type'] = 'passport'
        return jsonify(data), 200
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
