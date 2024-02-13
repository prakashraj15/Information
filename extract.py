import cv2
import numpy as np
import supervision as sv
import pytesseract


def crop_ocr(image, detection):
    bounding_box = detection[0]
    x_min, y_min, x_max, y_max = map(int, bounding_box)
    cropped_box = image[y_min:y_max, x_min:x_max]
    scale = 1
    cropped_box = cv2.resize(cropped_box, (0, 0), fx=scale, fy=scale)
    text = pytesseract.image_to_string(cropped_box)
    return text.strip()


def on_prediction(predictions, image):
    labels = [(p["class"], p['confidence'])
              for p in predictions['predictions']]
    detections = sv.Detections.from_roboflow(predictions)
    text = [crop_ocr(image, detection) for detection in detections]

    max_confidence_predictions = {}
    for i, (label, confidence) in enumerate(labels):
        if label not in max_confidence_predictions or confidence > max_confidence_predictions[label]["confidence"]:
            max_confidence_predictions[label] = {
                'label': label, 'confidence': confidence, 'text': text[i]}
    data = dict()
    for key, value in max_confidence_predictions.items():
        if (value['text'] != ''):
            data[key] = value['text']
    return data
