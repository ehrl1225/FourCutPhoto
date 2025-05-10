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



