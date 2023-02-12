#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
from PIL import Image

class ImageGrabber():
    def __init__(self, cameraId=0):
        self.cameraId = cameraId
        self.cam = None

    def __enter__(self):
        self.cam = cv2.VideoCapture(self.cameraId)
        return self

    def get_images(self):
        if(self.cam == None):
            print("You must first open the camera!")
            return
        while True:
            ret, frame = self.cam.read()
            if not ret:
                print("failed to grab frame")
                break

            color_converted = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_image=Image.fromarray(color_converted)
            yield pil_image
            

    def __exit__(self, *exc_info):
        self.cam.release()
        cv2.destroyAllWindows()
        self.cam = None
