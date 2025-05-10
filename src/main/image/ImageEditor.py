from src.main.util import FourCutData
import numpy as np
import cv2

from src.main.util.PhotoRect import PhotoRect


class ImageEditor:

    def __init__(self):
        pass

    def resizeWithRatio(self, image:np.ndarray, target_width:int, target_height:int) -> np.ndarray:
        image_height, image_width, _ = image.shape
        width_ratio = target_width / image_width
        height_ratio = target_height / image_height
        if width_ratio >= height_ratio:
            fixed_width = target_width
            fixed_height = int(image_height * width_ratio)
            return cv2.resize(image, (fixed_width, fixed_height))
        else:
            fixed_width = int(image_width * height_ratio)
            fixed_height = target_height
            return cv2.resize(image, (fixed_width, fixed_height))

    def cutOverSize(self, image:np.ndarray, target_width:int, target_height:int) -> np.ndarray:
        image_height, image_width, _ = image.shape
        if image_width > target_width:
            diff = image_width - target_width
            width_start = int(diff / 2)
            width_end = width_start + target_width
            return image[:, width_start:width_end]
        elif image_height > target_height:
            diff = image_height - target_height
            height_start = int(diff / 2)
            height_end = height_start + target_height
            return image[height_start:height_end, :]
        return image

    def overwriteImage(self, canvas: np.ndarray, photo: np.ndarray, photo_rect: PhotoRect):
        start_y = photo_rect.start_y
        end_y = photo_rect.end_y
        start_x = photo_rect.start_x
        end_x = photo_rect.end_x

        # Check if the photo has an alpha channel
        if photo.shape[2] == 4:  # RGBA image
            alpha_channel = photo[:, :, 3] / 255.0  # Normalize alpha to range [0, 1]
            for c in range(3):  # Iterate over RGB channels
                canvas[start_y:end_y, start_x:end_x, c] = (
                    alpha_channel * photo[:, :, c] +
                    (1 - alpha_channel) * canvas[start_y:end_y, start_x:end_x, c]
                )
        else:  # No alpha channel, overwrite directly
            canvas[start_y:end_y, start_x:end_x] = photo

    def editImage(self, four_cut_data:FourCutData, photos:list[np.ndarray]) -> np.ndarray:
        canvas = four_cut_data.photo.copy()
        for photo_rect_index, photo_rect in enumerate(four_cut_data.photo_rects):
            width = photo_rect.end_x - photo_rect.start_x
            height = photo_rect.end_y - photo_rect.start_y
            photo = photos[photo_rect_index]
            fixed_size_image = self.resizeWithRatio(photo, width, height)
            cut_image = self.cutOverSize(fixed_size_image, width, height)
            self.overwriteImage(canvas, cut_image, photo_rect)
        return canvas

