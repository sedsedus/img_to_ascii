#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2

class FrameGrabber():
    def __init__(self, cameraId=0):
        self.cameraId = cameraId
        self.cam = None

    def __enter__(self):
        self.cam = cv2.VideoCapture(self.cameraId)
        return self

    def get_frames(self):
        if(self.cam == None):
            print("You must first open the camera!")
            return
        while True:
            ret, frame = self.cam.read()
            if not ret:
                print("failed to grab frame")
                break
            yield frame
            

    def __exit__(self, *exc_info):
        self.cam.release()
        cv2.destroyAllWindows()
        self.cam = None
