from src.main.image import ImageEditor, PhotoRect
from src.main.util import DataManager
import cv2
import os


def imageEditorTest():
    DataManager.base_path = "."
    dataManager = DataManager()
    dataManager.loadFourCutDatas()

    imageEditor = ImageEditor()
    images = list()
    for i in os.listdir("src/test/photos"):
        img_path = os.path.join("src/test/photos", i)
        images.append(cv2.imread(img_path))
    edited_image = imageEditor.editImage(dataManager.four_cut_datas[0], images)
    cv2.imwrite(os.path.join(DataManager.base_path, "dest", "1.jpg"), edited_image)

def imageEditorTest2():
    imageEditor = ImageEditor()
    frame_img = cv2.imread("img/frame2.jpeg")
    overlay_img1 = cv2.imread("overlay_img/frame2/2.png", cv2.IMREAD_UNCHANGED)
    overlay_img2 = cv2.imread("overlay_img/frame2/4.png", cv2.IMREAD_UNCHANGED)
    overlay_img3 = cv2.imread("overlay_img/frame2/3.png", cv2.IMREAD_UNCHANGED)
    overlay_img4 = cv2.imread("overlay_img/frame2/1.png", cv2.IMREAD_UNCHANGED)
    photo_rect1 = PhotoRect(44,  604,314, 1029)
    photo_rect2 = PhotoRect(15, 1184, 343, 1666)
    photo_rect3 = PhotoRect(793, 317, 1122, 735)
    photo_rect4 = PhotoRect(610, 947, 890, 1372)

    width1 = photo_rect1.end_x - photo_rect1.start_x
    width2 = photo_rect2.end_x - photo_rect2.start_x
    width3 = photo_rect3.end_x - photo_rect3.start_x
    width4 = photo_rect4.end_x - photo_rect4.start_x
    height1 = photo_rect1.end_y - photo_rect1.start_y
    height2 = photo_rect2.end_y - photo_rect2.start_y
    height3 = photo_rect3.end_y - photo_rect3.start_y
    height4 = photo_rect4.end_y - photo_rect4.start_y
    fixed_size_image1 = imageEditor.resizeWithRatio(overlay_img1, width1, height1)
    fixed_size_image2 = imageEditor.resizeWithRatio(overlay_img2, width2, height2)
    fixed_size_image3 = imageEditor.resizeWithRatio(overlay_img3, width3, height3)
    fixed_size_image4 = imageEditor.resizeWithRatio(overlay_img4, width4, height4)
    cut_image1 = imageEditor.cutOverSize(fixed_size_image1, width1, height1)
    cut_image2 = imageEditor.cutOverSize(fixed_size_image2, width2, height2)
    cut_image3 = imageEditor.cutOverSize(fixed_size_image3, width3, height3)
    cut_image4 = imageEditor.cutOverSize(fixed_size_image4, width4, height4)

    imageEditor.overwriteImage(frame_img, cut_image1, photo_rect1)
    imageEditor.overwriteImage(frame_img, cut_image2, photo_rect2)
    imageEditor.overwriteImage(frame_img, cut_image3, photo_rect3)
    imageEditor.overwriteImage(frame_img, cut_image4, photo_rect4)
    cv2.imshow("frame", frame_img)
    cv2.waitKey(0)

def imageEditorTest3():
    dataManager = DataManager()
    dataManager.loadFourCutDatas()
    four_cut_data = dataManager.four_cut_datas[0]
    imageEditor = ImageEditor()
    frame_img = imageEditor.editOverlayImage(four_cut_data, four_cut_data.photo)
    cv2.imshow("frame", frame_img)
    cv2.waitKey(0)

if __name__ == '__main__':
    imageEditorTest3()