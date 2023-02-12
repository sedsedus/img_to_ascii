#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
from convert import ImgConverter

def live_convert(imgConverter: ImgConverter, imgName = "img", cameraId=0):
    cam = cv2.VideoCapture(cameraId)
    print("Press 'Ctrl + c' to quit")

    try:
        while True:
            ret, frame = cam.read()
            if not ret:
                print("failed to grab frame")
                break
            
            cv2.imwrite(f'{imgName}.png', frame)
            imgConverter.generate_output(imgConverter.get_intensities(f"{imgName}.png"), f"{imgName}.txt")  
            # cv2.imshow('frame', frame)
    except KeyboardInterrupt:
        print()
        print("Exiting...")

    cam.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    converter = ImgConverter()
    live_convert(converter)