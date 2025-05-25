from src.main.image import FourCutData
import matplotlib.pyplot as plt
from src.test.test_main import testCase, testAll
import numpy as np
import json
from src.main.image.PhotoRect import PhotoRect


def loadJsonDatas(photo: np.ndarray, json_file_path: str):
    with open(json_file_path) as json_file:
        data = json.load(json_file)
        photo_rects: list[PhotoRect] = []
        for photoRect in data["image_rect"]:
            start_x = photoRect["start_x"]
            start_y = photoRect["start_y"]
            end_x = photoRect["end_x"]
            end_y = photoRect["end_y"]
            photo_rect = PhotoRect(start_x, start_y, end_x, end_y)
            photo_rects.append(photo_rect)
        return FourCutData(photo, photo_rects)


@testCase("사진 테스트")
def test_FourCutData():
    image_path = "../img/test_4_cut.png"
    json_path = "../json/test_4_cut.json"
    image_array = plt.imread(image_path)
    json_data = loadJsonDatas(image_array, json_path)
    assert len(json_data.photo_rects) == 4



if __name__ == '__main__':
    testAll()