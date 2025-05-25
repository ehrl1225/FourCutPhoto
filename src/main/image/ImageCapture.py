import sys

import cv2
import numpy as np


class ImageCapture:
    displayCapture:bool = False
    cam_not_found = False
    cam_id:int = 0

    def __init__(self):
        pass

    def __del__(self):
        self.cam.release()
        if self.displayCapture:
            cv2.destroyAllWindows()

    def openCamera(self):
        self.cam = cv2.VideoCapture(self.cam_id)

    def closeCamera(self):
        self.cam.release()

    def capture(self) -> np.ndarray | None:
        ret, frame = self.cam.read()
        if not ret:
            if not self.cam_not_found:

                print("Camera not found", file=sys.stderr)
                self.cam_not_found = True
            return None
        self.cam_not_found = False
        return frame

    def save_image(self, image_path:str, image:np.ndarray):
        cv2.imwrite(image_path, image)

    def save_video(self, video_path:str, video:cv2.VideoWriter):
        pass

    def showCapture(self):
        self.displayCapture = True
        while cv2.waitKey(1) != ord('q'):
            ret, frame = self.cam.read()
            cv2.imshow('Capture', frame)

    def saveVideo(self):
        pass
