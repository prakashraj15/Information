
# Identity Card Text Extraction
## Introduction
Information extraction from Indian ID cards (Aadhaar, PAN, Passport). This application aims to reduce human typing workload and saves more time.

## Steps

#### 1) Classification  
A Convolutional Neural Network (CNN) is employed for the task of ID card classification

#### 2) Object Detection 
Object detection is implemented using YOLOv7 (You Only Look Once version 7). YOLO is a real-time object detection system known for its speed and accuracy.

#### 3) Text Extraction
For extracting text information from the ID card images, PyTesseract is utilized. PyTesseract is a Python wrapper for Google's Tesseract-OCR Engine, which is an Optical Character Recognition (OCR) tool.
