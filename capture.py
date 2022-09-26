import cv2
from main import get_intensities, generate_output

cam = cv2.VideoCapture(0)
imgName = "img"
while True:
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break
    
    cv2.imwrite(f'{imgName}.png', frame)
    generate_output(get_intensities(f"{imgName}.png"), f"{imgName}.txt")

cam.release()
cv2.destroyAllWindows()
