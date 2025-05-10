import os
import sys

import cv2
from PyQt6.QtGui import QImage

from .FourCutData import FourCutData
from .PhotoRect import PhotoRect
import json
import numpy as np
import datetime

import hashlib
def get_hash_value(in_str, in_digest_bytes_size=64, in_return_type='digest'):
    """해시값을 구한다
    Parameter: in_str: 해싱할문자열, in_digest_bytes_size: Digest바이트크기,
               in_return_type: 반환형태(digest or hexdigest or number) """
    assert 1 <= in_digest_bytes_size and in_digest_bytes_size <= 64
    blake  = hashlib.blake2b(in_str.encode('utf-8'), digest_size=in_digest_bytes_size)
    if in_return_type == 'hexdigest': return blake.hexdigest()
    elif in_return_type == 'number': return int(blake.hexdigest(), base=16)
    return blake.digest()

START_X = "start_x"
START_Y = "start_y"
END_X = "end_x"
END_Y = "end_y"
IMAGE_RECT = "image_rect"
OVERLAY_RECT = "overlay_rect"
IMAGE_FILE = "image_file"

class DataManager:
    """
    사용자의 임시 파일을 저장하고 삭제하거나 네 컷 템플릿을 가져올 때 사용합니다.
    """
    base_path = "./"
    image_path:str = "img/"
    json_path:str = "json/"
    overlay_path:str = "overlay_img/"
    result_image_source:str = "result/image/source/"
    result_image_destination:str = "result/image/destination/"
    photo_save_dir_name:str
    photo_save_dir_path:str
    images:list[np.ndarray] = list()
    four_cut_datas : list[FourCutData] = list()
    people_count : int = 1
    selected_frame_index: int = 0
    edited_image:np.ndarray
    
    def __init__(self):
        pass

    def setEditedImage(self, edited_image:np.ndarray):
        self.edited_image = edited_image

    def getEditedImage(self):
        return self.edited_image

    def setSelectedFrameIndex(self, selected_frame_index):
        self.selected_frame_index = selected_frame_index

    def getSelectedFrameIndex(self):
        return self.selected_frame_index

    def saveImageDestination(self, image):
        path = os.path.join(self.base_path, self.result_image_destination, self.photo_save_dir_name+".png")
        cv2.imwrite(path, image)

    def setPeopleCount(self, people_count):
        self.people_count = people_count

    def getFourCutDatas(self):
        return self.four_cut_datas

    @staticmethod
    def checkPath():
        image_dir_path = os.path.join(DataManager.base_path, DataManager.image_path)
        json_dir_path = os.path.join(DataManager.base_path, DataManager.json_path)
        overlay_dir_path = os.path.join(DataManager.base_path, DataManager.overlay_path)
        if not os.path.exists(image_dir_path):
            os.mkdir(image_dir_path)
        if not os.path.exists(json_dir_path):
            os.mkdir(json_dir_path)
        if not os.path.exists(overlay_dir_path):
            os.mkdir(overlay_dir_path)


    def loadFourCutDatas(self) -> None:
        image_path = os.path.join(DataManager.base_path, DataManager.image_path)
        json_path = os.path.join(DataManager.base_path, DataManager.json_path)
        overlay_path = os.path.join(DataManager.base_path, DataManager.overlay_path)
        four_cut_images = os.listdir(image_path)
        four_cut_datas:list[FourCutData] = list()

        for image in four_cut_images:
            img = cv2.imread(os.path.join(image_path, image))
            img_name = os.path.splitext(image)[0]

            new_json_path = os.path.join(json_path, f"{img_name}.json")
            if not os.path.isfile(new_json_path):
                print(f"can't find json file from {new_json_path}" , file=sys.stderr)
                continue
            four_cut_data = self.loadJsonDatas(img, new_json_path)

            overlay_img_path = os.path.join(overlay_path, img_name)
            overlay_images = self.loadOverlayImages(overlay_img_path, four_cut_data.getOverlayImageFiles())
            four_cut_data.setOverlayImages(overlay_images)

            four_cut_datas.append(four_cut_data)
        self.four_cut_datas = four_cut_datas

    def loadJsonDatas(self, photo:np.ndarray, json_file_path:str):
        with open(json_file_path) as json_file:
            data = json.load(json_file)
            photo_rects: list[PhotoRect] = []
            overlay_rects: list[PhotoRect] = []
            overlay_files: list[str] = []
            for photoRect in data[IMAGE_RECT]:
                start_x = photoRect[START_X]
                start_y = photoRect[START_Y]
                end_x = photoRect[END_X]
                end_y = photoRect[END_Y]
                photo_rect = PhotoRect(start_x, start_y, end_x, end_y)
                photo_rects.append(photo_rect)

            if OVERLAY_RECT in data:
                for overlayRect in data[OVERLAY_RECT]:
                    file_name = overlayRect[IMAGE_FILE]
                    start_x = overlayRect[START_X]
                    start_y = overlayRect[START_Y]
                    end_x = overlayRect[END_X]
                    end_y = overlayRect[END_Y]
                    photo_rect = PhotoRect(start_x, start_y, end_x, end_y)
                    overlay_rects.append(photo_rect)
                    overlay_files.append(file_name)
        four_cut_data = FourCutData(photo, photo_rects)
        four_cut_data.setOverlayImageFiles(overlay_files)
        four_cut_data.setOverlayRects(overlay_rects)

        return four_cut_data

    def loadOverlayImages(self, overlay_folder_path:str, overlay_files:list[str]) -> list[np.ndarray]:
        images:list[np.ndarray] = list()
        for overlay_file in overlay_files:
            image_path = os.path.join(overlay_folder_path, overlay_file)
            image = cv2.imread(image_path)
            images.append(image)
        return images


    def makePhotoDirectory(self):
        now = datetime.datetime.now()
        now_str = now.strftime("%Y%m%d%H%M%S")
        photo_dir_name = get_hash_value(in_str=now_str, in_digest_bytes_size=10, in_return_type='hexdigest')
        base_path = DataManager.base_path
        result_image_source = DataManager.result_image_source
        result_image_source_path = os.path.join(base_path, result_image_source)
        photo_dir_path = os.path.join(result_image_source_path, photo_dir_name)
        os.makedirs(photo_dir_path, exist_ok=True)
        self.photo_save_dir_name = photo_dir_name
        self.photo_save_dir_path = photo_dir_path

    def setPhotoDirectory(self, photo_dir_name):
        """
        to test gui
        :param photo_dir_name:
        :return:
        """
        base_path = DataManager.base_path
        result_image_source = DataManager.result_image_source
        result_image_source_path = os.path.join(base_path, result_image_source)
        photo_dir_path = os.path.join(result_image_source_path, photo_dir_name)
        self.photo_save_dir_name = photo_dir_name
        self.photo_save_dir_path = photo_dir_path
        self.clearImages()
        photo_paths = self.getPhotoPaths()
        for photo_path in photo_paths:
            image = cv2.imread(photo_path)
            self.images.append(image)

    def saveQImage(self, image:QImage, index:int):
        image.save(os.path.join(self.photo_save_dir_path, f"{str(index)}.png"))

    def getPhotoPaths(self):
        photo_path_list = []
        for file_number in range(1,7):
            filename = f"{file_number}.png"
            file_path = os.path.join(self.photo_save_dir_path, filename)
            photo_path_list.append(file_path)
        return photo_path_list

    def clearImages(self):
        self.images.clear()

    def getImages(self):
        return self.images

