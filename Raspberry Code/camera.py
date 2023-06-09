#!/usr/bin/python3

# Configure a raw stream and capture an image from it.
import libcamera
import torch
from picamera2 import Picamera2, Preview
import numpy as np
import onnxruntime
import time
import torchvision
import matplotlib.pyplot as plt
import os
from libcamera import Transform
import display_library as dl
from signs import signs, get_area
from yolo import YOLOv8

# initialize the picamera
def init_camera():
    picam2 = Picamera2()
    picam2.start()
    return picam2

# load the yolov8 model
def init_model(model):
    yolov8_detector = YOLOv8(model, conf_thres=0.2, iou_thres=0.3)
    return yolov8_detector

# take a frame from the camera, prepare it for inference, and run inference
def run_inference(camera, detector):
    t = time.time()
    raw = camera.capture_array()
    # we need to flip the image since the camera is upside down on the car
    # picamera gives a dummy 4th channel, filled with 255, which we remove
    # moreover, we add an extra BATCH dimension, and move the channel dimension to where the model expects it
    image = (np.fliplr(np.flipud(np.float32(raw))) / 255.0)[np.newaxis, :, :, 0:3].transpose(0, 3, 1, 2)
    results = detector(image)
    t2 = time.time()
    print(f'{t2 - t}s')
    return results

# returns the closest traffic signs from all the detected traffic signs
# uses the area of the bounding box to judge distance, since a further traffic sign
# usually has a smaller area
def get_closest_result(results):
    boxes, confidences, classes = results
    
    largest_area = 0
    closest_result = None
    for box, confidence, classs in zip(boxes, confidences, classes):
        area = get_area((box, confidence, classs))
        if area > largest_area:
            largest_area = area
            closest_result = (box, confidence, classs)

    return closest_result

model = "best_v8.onnx"
