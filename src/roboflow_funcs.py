import os
import cv2
import tempfile
import numpy as np
from roboflow import Roboflow
from PIL import Image

def roboflow_setup():
    api_key = "BlAwqBsDmqmKzgsnFvWr"
    if api_key is None:
        api_key = "BlAwqBsDmqmKzgsnFvWr"
    rf = Roboflow(api_key=api_key)
    project = rf.workspace("building-eezen").project("building-outline-lzowe")
    model = project.version(1).model
    return model

def roboflow_segmentation(model, img):
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    temp_path = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False).name
    Image.fromarray(img_rgb).save(temp_path)

    result = model.predict(temp_path, confidence=40).json()

    os.remove(temp_path)

    combined_mask = np.zeros(img.shape[:2], dtype=np.uint8)
    for pred in result['predictions']:
        if 'points' in pred:
            points = np.array([[p['x'], p['y']] for p in pred['points']], dtype=np.int32)
            mask = np.zeros(img.shape[:2], dtype=np.uint8)
            cv2.fillPoly(mask, [points], 255)
            combined_mask = cv2.bitwise_or(combined_mask, mask)

    masked_image = cv2.bitwise_and(img, img, mask=combined_mask)

    return masked_image

