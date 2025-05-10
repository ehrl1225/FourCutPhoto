import numpy as np


class PhotoList(object):
    photos:list[np.ndarray]

    def __init__(self):
        self.photos = list()

    def addPhoto(self, photo:np.ndarray):
        self.photos.append(photo)

