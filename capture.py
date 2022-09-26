import cv2
import sys
import time
cam = cv2.VideoCapture(0)

while True:
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break
    cv2.imwrite('opencv.png', frame)
    time.sleep(0.1)

cam.release()
cv2.destroyAllWindows()
