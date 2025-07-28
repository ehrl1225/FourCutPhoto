from image import ImageEditor
from src.main.image import ImageCapture
import cv2

def imageCaptureTest():
    image = ImageCapture()
    image_editor = ImageEditor()
    image.setCam(2)
    image.openCamera()
    while True:
        img = image.capture()
        img = image_editor.cutUpAndDownImage(img, 95)
        cv2.imshow('image', img)
        if cv2.waitKey(1) == ord('q'):
            break



if __name__ == '__main__':
    imageCaptureTest()