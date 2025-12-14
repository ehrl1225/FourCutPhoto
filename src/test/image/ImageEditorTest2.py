
from image import ImageEditor
import cv2


def main():
    imageEditor = ImageEditor()
    img = cv2.imread("img.JPG")
    width = 1176
    height = 1776
    img = imageEditor.resizeWithRatio(img, width, height)
    cv2.imwrite("resized_img.JPG", img)



if __name__ == '__main__':
    main()