import json

import numpy as np
from numpy import ndarray

from .PhotoRect import PhotoRect


class FourCutData:
    photo_rects:list[PhotoRect]
    photo:np.ndarray
    overlay_rects:list[PhotoRect]
    overlay_images:list[np.ndarray]
    overlay_image_files:list[str]
    overlay_on_cam:bool = False

    def __init__(self,photo:ndarray, photo_rects:list[PhotoRect]):
        self.photo = photo
        self.photo_rects = photo_rects

    def setOverlayRects(self, overlay_rects:list[PhotoRect]):
        self.overlay_rects = overlay_rects

    def setOverlayImages(self, overlay_images:list[np.ndarray]):
        self.overlay_images = overlay_images

    def setOverlayImageFiles(self, overlay_image_files:list[str]):
        self.overlay_image_files = overlay_image_files

    def getOverlayImageFiles(self):
        return self.overlay_image_files

    def hasOverlayImages(self):
        return len(self.overlay_image_files) > 0

    def overlayOnCam(self):
        return self.overlay_on_cam

    def getOverlayImageCount(self):
        return len(self.overlay_image_files)

    def getRelativeOverlayPhotoRect(self, index:int) -> PhotoRect:
        photo_rect = self.photo_rects[index]
        overlay_rect = self.overlay_rects[index]
        start_x = overlay_rect.start_x - photo_rect.start_x
        end_x = start_x + overlay_rect.getWidth()
        start_y = overlay_rect.start_y - photo_rect.start_y
        end_y = start_y + overlay_rect.getHeight()

        relative_photo_rect = PhotoRect(start_x, start_y, end_x, end_y)
        return relative_photo_rect

    def copy(self):
        return FourCutData(self.photo, self.photo_rects)
