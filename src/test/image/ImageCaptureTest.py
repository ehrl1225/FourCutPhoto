from src.main.image import ImageCapture
import cv2

def imageCaptureTest():
    image = ImageCapture()
    image.setCam(2)
    image.openCamera()
    while True:
        img = image.capture()
        cv2.imshow('image', img)
        if cv2.waitKey(1) == ord('q'):
            break



if __name__ == '__main__':
    imageCaptureTest()