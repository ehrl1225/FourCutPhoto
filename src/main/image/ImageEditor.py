from .FourCutData import FourCutData
from .PhotoRect import PhotoRect
import numpy as np
import cv2



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

    def getSizeRatio(self, image:np.ndarray, photo_rect:PhotoRect):
        image_height, image_width, _ = image.shape
        image_ratio = image_width / image_height

        frame_width = photo_rect.getWidth()
        frame_height = photo_rect.getHeight()
        frame_ratio = frame_width / frame_height

        if frame_ratio >= image_ratio:
            return image_width / frame_width
        else:
            return image_height / frame_height

    def cutWithRatio(self, image:np.ndarray, photo_rect:PhotoRect) -> np.ndarray:
        """
        :param image:
        :param photo_rect: get mutated in this function
        :return:
        """
        image_height, image_width, _ = image.shape
        image_ratio = image_width / image_height

        frame_width = photo_rect.getWidth()
        frame_height = photo_rect.getHeight()
        frame_ratio = frame_width / frame_height

        def setPhotoRect(rect:PhotoRect, start_x:int, start_y:int, end_x:int, end_y:int):
            rect.start_x = start_x
            rect.end_x = end_x
            rect.start_y = start_y
            rect.end_y = end_y


        if frame_ratio >= image_ratio:
            fixed_height = int(image_width / frame_ratio)
            start_x = 0
            start_y = int((image_height - fixed_height) / 2)
            end_x = image_width
            end_y = start_y + fixed_height
            setPhotoRect(photo_rect, start_x, start_y, end_x, end_y)
            return image[start_y:end_y, start_x:end_x]
        else:
            fixed_width = int(image_height * frame_ratio)
            start_x = int((image_width - fixed_width) / 2)
            start_y = 0
            end_x = start_x + fixed_width
            end_y = image_height
            setPhotoRect(photo_rect, start_x, start_y, end_x, end_y)
            return image[start_y:end_y, start_x:end_x]

    def cutOverSizedOverlay(self, image_photo_rect:PhotoRect, overlay_relative_photo_rect:PhotoRect, overlay_image:np.ndarray):
        image_height = image_photo_rect.getHeight()
        image_width = image_photo_rect.getWidth()
        overlay_img = overlay_image.copy()
        if overlay_relative_photo_rect.start_x < 0:
            overlay_img = overlay_img[:, -overlay_relative_photo_rect.start_x:]
            overlay_relative_photo_rect.start_x = 0
        if overlay_relative_photo_rect.end_x >= image_width:
            diff = overlay_relative_photo_rect.end_x - image_width
            overlay_img = overlay_img[:, :-diff]
            overlay_relative_photo_rect.end_x = image_width
        if overlay_relative_photo_rect.start_y < 0:
            overlay_img = overlay_img[-overlay_relative_photo_rect.start_y:, :]
            overlay_relative_photo_rect.start_y = 0
        if overlay_relative_photo_rect.end_y >= image_height:
            diff = overlay_relative_photo_rect.end_y - image_height
            overlay_img = overlay_img[:-diff, :]
            overlay_relative_photo_rect.end_y = image_height
        return overlay_img


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
            # Determine if the photo is in [0,1] float range or [0,255] range.
            # np.nanmax ignores NaN values for the max calculation.
            max_val = np.nanmax(photo)
            is_float_normalized = photo.dtype.kind == 'f' and max_val <= 1.0

            photo_to_blend = photo.astype(np.float32)
            photo_rgb = photo_to_blend[:, :, :3]

            if is_float_normalized:
                # Values are in [0,1], so use alpha directly and scale RGB up to 255.
                alpha_channel = photo_to_blend[:, :, 3]
                photo_rgb = photo_rgb * 255
            else:
                # Values are in [0,255], so normalize alpha and use RGB directly.
                alpha_channel = photo_to_blend[:, :, 3] / 255.0

            for c in range(3):  # Iterate over RGB channels
                # Perform alpha blending.
                blend_result = (
                    alpha_channel * photo_rgb[:, :, c] +
                    (1 - alpha_channel) * canvas[start_y:end_y, start_x:end_x, c]
                )

                # Find where the blending result is NaN
                nan_mask = np.isnan(blend_result)
                original_pixels = canvas[start_y:end_y, start_x:end_x, c]

                # Replace NaN values with the original canvas pixels.
                blend_result[nan_mask] = original_pixels[nan_mask]

                # Clip the result and assign back to the canvas.
                canvas[start_y:end_y, start_x:end_x, c] = np.clip(blend_result, 0, 255)
        else:  # No alpha channel, overwrite directly
            canvas[start_y:end_y, start_x:end_x] = photo

    def editImage(self, four_cut_data:FourCutData, photos:list[np.ndarray]) -> np.ndarray:
        canvas = four_cut_data.photo.copy()
        for photo_rect_index, photo_rect in enumerate(four_cut_data.photo_rects):
            width = photo_rect.getWidth()
            height = photo_rect.getHeight()
            photo = photos[photo_rect_index]
            fixed_size_image = self.resizeWithRatio(photo, width, height)
            cut_image = self.cutOverSize(fixed_size_image, width, height)
            self.overwriteImage(canvas, cut_image, photo_rect)
        return canvas

    def editOverlayImage(self, four_cut_data:FourCutData, image:np.ndarray) -> np.ndarray:
        canvas = image.copy()
        for photo_rect_index, photo_rect in enumerate(four_cut_data.overlay_rects):
            width = photo_rect.getWidth()
            height = photo_rect.getHeight()
            photo = four_cut_data.overlay_images[photo_rect_index]
            fixed_size_image = self.resizeWithRatio(photo, width, height)
            cut_image = self.cutOverSize(fixed_size_image, width, height)
            self.overwriteImage(canvas, cut_image, photo_rect)
        return canvas

    def cutUpAndDownImage(self, image:np.ndarray, height:int) -> np.ndarray:
        canvas = image.copy()
        image_height, image_width, _ = image.shape
        cropped_canvas = canvas[height:-height, :]
        return cropped_canvas

