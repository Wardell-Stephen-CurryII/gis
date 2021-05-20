import cv2
import numpy as np
from PIL import Image


# 定位文字位置
def picture_detection(img_path):
    img_001 = cv2.imread(img_path)
    # cv2.imshow('img_001', img_001)
    img = Image.open(img_path)  # 打开图片
    im = img.convert('RGB')
    pix = im.load()  # 导入像素
    width = im.size[0]  # 获取宽度
    height = im.size[1]  # 获取长度
    for x in range(width):
        for y in range(height):
            rgba = im.getpixel((x, y))
            if rgba[0] in range(181, 191) and rgba[1] in range(181, 191) and rgba[2] in range(170, 180):
                im.putpixel((x, y), (252, 249, 242))
            elif rgba[0] in range(250, 256) and rgba[1] in range(250, 256) and rgba[2] in range(250, 256):
                im.putpixel((x, y), (252, 249, 242))
            else:
                continue
    img_ = np.array(im)
    cv2.imshow('img', img_)
    cv2.waitKey(0)
    # img = cv2.imread(img_path)
    # 转换灰度并去噪声
    gray = cv2.cvtColor(img_, cv2.COLOR_BGR2GRAY)
    # 提取图像的梯度
    # 以Sobel算子计算x，y方向上的梯度，之后在x方向上减去y方向上的梯度，通过这个减法，留下具有高水平梯度和低垂直梯度的图像区域
    gradX = cv2.Sobel(gray, ddepth=cv2.CV_32F, dx=1, dy=0)
    gradY = cv2.Sobel(gray, ddepth=cv2.CV_32F, dx=0, dy=1)

    gradient = cv2.subtract(gradX, gradY)
    gradient = cv2.convertScaleAbs(gradient)

    blurred = cv2.GaussianBlur(gradient, (9, 9), 0)
    (_, thresh) = cv2.threshold(blurred, 90, 255, cv2.THRESH_BINARY)
    cv2.imshow('blurred', blurred)
    cv2.imshow('thresh', thresh)
    # 建立一个椭圆核函数
    # kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (25, 25))

    # 执行图像形态学
    # closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    # cv2.imshow('closed0', closed)
    # cv2.waitKey(0)
    # closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    # cv2.imshow('closed0', closed)
    # cv2.waitKey(0)
    closed_4 = cv2.dilate(thresh, None, iterations=4)
    cv2.imshow('closed1', closed_4)
    cv2.waitKey(0)
    closed = cv2.erode(closed_4, None, iterations=6)
    cv2.imshow('closed2', closed)
    cv2.waitKey(0)
    closed = cv2.dilate(closed, None, iterations=3)
    # closed = cv2.erode(closed, None, iterations=2)
    # closed = cv2.dilate(closed, None, iterations=4)
    cv2.imshow('closed3', closed)
    cv2.waitKey(0)
    closed111 = cv2.dilate(closed, None, iterations=2)
    # closed = cv2.erode(closed, None, iterations=2)
    cv2.imshow('closed111', closed111)
    cv2.waitKey(0)
    # 使用mask更好用（也就是closed111）
    cv2.imwrite('data/result/R000183C1_C00034AE0_mask1.png', thresh)
    cv2.imwrite('data/result/R000183C1_C00034AE0_mask2.png', closed_4)
    cv2.imwrite('data/result/R000183C1_C00034AE0_mask3.png', closed111)
    (img_01, cnts, hierarchy) = cv2.findContours(closed.copy(),
                                    cv2.RETR_LIST,
                                    cv2.CHAIN_APPROX_SIMPLE)
    # print(img_01)
    # print(cnts)
    # print(hierarchy)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
    box_gather = []
    for i in range(len(cnts)):
        c = cnts[i]
        # print(c)
        # 计算轮廓旋转后的边框
        rect = cv2.minAreaRect(c)
        # print(rect)
        if -82 < rect[-1] < -7:
            continue
        else:
            box = np.int0(cv2.boxPoints(rect))
            box_gather.append(box)

    # 在原始图像绘制检测边框
    draw_img = cv2.drawContours(img_.copy(), box_gather, -1, (0, 0, 255), 3)
    cv2.imshow('draw_img', draw_img)
    cv2.waitKey(0)
    # cv2.imwrite('data/result/R000183BA_C00034AD9_mask.png',draw_img)
    return box_gather


if __name__ == '__main__':
    path = 'data/picture_merge/R000183C1_C00034AE0.png'
    # path = 'data/result/pj/pj_90.png'
    box = picture_detection(path)
    # print(box)