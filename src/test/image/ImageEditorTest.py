from src.main.image import ImageEditor
from src.main.util import DataManager, PhotoRect
import cv2
import os


def imageEditorTest():
    DataManager.base_path = "src/test"
    dataManager = DataManager()
    fourCutData = dataManager.loadFourCutDatas()

    imageEditor = ImageEditor()
    images = list()
    for i in os.listdir("src/test/photos"):
        img_path = os.path.join("src/test/photos", i)
        images.append(cv2.imread(img_path))
    edited_image = imageEditor.editImage(fourCutData[0], images)
    cv2.imwrite(os.path.join(DataManager.base_path, "dest", "1.jpg"), edited_image)

def imageEditorTest2():
    imageEditor = ImageEditor()
    frame_img = cv2.imread("img/frame2.jpeg")
    overlay_img = cv2.imread("overlay_img/frame2/1.png", cv2.IMREAD_UNCHANGED)
    photo_rect = PhotoRect(44,  604,314, 1029)
    width = photo_rect.end_x - photo_rect.start_x
    height = photo_rect.end_y - photo_rect.start_y
    fixed_size_image = imageEditor.resizeWithRatio(overlay_img, width, height)
    cut_image = imageEditor.cutOverSize(fixed_size_image, width, height)

    imageEditor.overwriteImage(frame_img, cut_image, photo_rect)
    cv2.imshow("frame", frame_img)
    cv2.waitKey(0)

if __name__ == '__main__':
    imageEditorTest2()