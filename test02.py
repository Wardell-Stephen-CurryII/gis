import cv2
import numpy as np
from PIL import Image
from skimage import measure

# path = 'data/result/R000183C1_C00034AE0_inpaint.png'/
path = 'data/inpaint/R000183B3_C00034AD8_inpaint.png'
path_y = 'data/picture_merge/R000183B3_C00034AD8.png'
img_y = cv2.imread(path_y)
# print(img_y)
cv2.imshow('img_y', img_y)
cv2.waitKey(0)
# print(1)
img = Image.open(path)  # 打开图片
im = img.convert('RGB')
img_ = np.array(im)
cv2.imshow('img_', img_)
cv2.waitKey(0)
pix = im.load()  # 导入像素
width = im.size[0]  # 获取宽度
height = im.size[1]  # 获取长度
for x in range(width):
    for y in range(height):
        # 获取各点像素
        rgb = im.getpixel((x, y))
        if rgb[0] in range(238, 246) and rgb[1] in range(240, 245) and rgb[2] in range(232, 238):
            # 在各点复制新颜色黑色
            im.putpixel((x, y), (255, 255, 255))
        elif rgb[0] in range(248, 250) and rgb[1] == 245 and rgb[2] == 238:
            im.putpixel((x, y), (255, 255, 255))
        elif rgb[0] in range(238, 241) and rgb[1] in range(232, 236) and rgb[2] in range(235, 238):
            im.putpixel((x, y), (255, 255, 255))
        elif rgb[0] in range(240, 244) and rgb[1] in range(239, 242) and rgb[2] == 236:
            im.putpixel((x, y), (255, 255, 255))
        elif rgb[0] in range(220, 229) and rgb[1] in range(232, 238) and rgb[2] in range(232, 236):
            im.putpixel((x, y), (255, 255, 255))
        elif rgb[0] in range(220, 223) and rgb[1] in range(232, 241) and rgb[2] in range(246, 253):
            im.putpixel((x, y), (255, 255, 255))
        elif rgb[0] in range(225, 229) and rgb[1] in range(232, 235) and rgb[2] in range(229, 233):
            im.putpixel((x, y), (255, 255, 255))
        elif rgb[0] in range(228, 239) and rgb[1] in range(235, 241) and rgb[2] in range(210, 223):
            im.putpixel((x, y), (255, 255, 255))
        elif rgb[0] in range(239, 244) and rgb[1] in range(232, 238) and rgb[2] in range(222, 232):
            im.putpixel((x, y), (255, 255, 255))
        elif rgb[0] in range(213, 220) and rgb[1] in range(228, 236) and rgb[2] in range(208, 237):
            im.putpixel((x, y), (255, 255, 255))
        else:
            # 白色
            im.putpixel((x, y), (0, 0, 0))
# 转化灰度图
im = im.convert('L')
im_cv = np.array(im)
cv2.imshow('im_cv', im_cv)
cv2.waitKey(0)
# 去除噪声
blur = cv2.medianBlur(im_cv, 5)
cv2.imshow('blur', blur)
cv2.waitKey(0)
kernel = np.ones((5, 5), np.uint8)
# image = cv2.imread(im_cv)
# gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
# gradient = cv2.morphologyEx(blur, cv2.MORPH_GRADIENT, kernel)
# cv2.imshow('gradient', gradient)
# cv2.waitKey(0)
# 顶帽
# tophat = cv2.morphologyEx(im_cv, cv2.MORPH_TOPHAT, kernel)
# cv2.imshow('tophat', tophat)
# cv2.waitKey(0)
# 黑帽
# blackhat = cv2.morphologyEx(im_cv, cv2.MORPH_BLACKHAT, kernel)
# cv2.imshow('blackhat', blackhat)
# cv2.waitKey(0)
dilate = cv2.dilate(blur, None, iterations=4)  # 膨胀
cv2.imshow('dilate', dilate)
cv2.waitKey(0)
erode = cv2.erode(dilate, None, iterations=3)  # 腐蚀
cv2.imshow('erode', erode)
cv2.waitKey(0)
# _, binary = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)

# dilate = cv2.dilate(blur, None, iterations=4) # 膨胀
# dilate = cv2.dilate(dilate, kernel, iterations=3) # 膨胀
# cv2.imshow('dilate1', dilate)
# cv2.waitKey(0)
# dilate = cv2.erode(dilate, None, iterations=4)  # 腐蚀
# cv2.imshow('dilate2', dilate)
# cv2.waitKey(0)

open = cv2.morphologyEx(erode, cv2.MORPH_OPEN, kernel)
open = cv2.morphologyEx(open, cv2.MORPH_OPEN, kernel)
# closing = cv2.morphologyEx(closing, cv2.MORPH_CLOSE, kernel)
cv2.imshow('open', open)
cv2.waitKey(0)
# print(open)
# dilate = cv2.erode(dilate, None, iterations=4)  # 腐蚀
# cv2.imshow('dilate3', dilate)
# cv2.waitKey(0)

# dilate = cv2.dilate(dilate, None, iterations=2) # 膨胀
# dilate = cv2.dilate(dilate, None, iterations=3)  # 腐蚀
# hierarchy代表着轮廓层级其中有4个数，[0]代表后一个轮廓、[1]代表前一个轮廓、[2]代表内嵌轮廓、[3]代表父轮廓
# _, contours, hierarchy = cv2.findContours(open, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
_, contours, hierarchy = cv2.findContours(open, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
# print(contours)
# for cont in contours:
#     hull = cv2.convexHull(cont)
#     # print(hull)
#     cv2.polylines(img_, [hull], True, (0, 255, 0), 2)
# cv2.imshow("result", img_)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

for cont in contours:
    # 取轮廓长度的0.015为epsilon 暂时最佳
    epsilon = 0.012 * cv2.arcLength(cont, True)
    # print(epsilon)
    epsilon_ = epsilon if epsilon <= 3 else 6
    # 预测多边形
    box = cv2.approxPolyDP(cont, epsilon_, True)
    # print(box)
    # print(box.shape)
    img_re = cv2.polylines(img_, [box], True, (0, 0, 255), 2)
cv2.imshow('img_re', img_re)
cv2.waitKey(0)


# 单张轮廓坐标,以及外接矩形数据
def box_data(self, path):
    img = Image.open(path)  # 打开图片
    im = img.convert('RGB')
    img_ = np.array(im)
    pix = im.load()  # 导入像素
    width = im.size[0]  # 获取宽度
    height = im.size[1]  # 获取长度
    for x in range(width):
        for y in range(height):
            # 获取各点像素
            rgba = im.getpixel((x, y))
            if rgba[0] in range(238, 246) and rgba[1] in range(240, 245) and rgba[2] in range(232, 238):
                # 在各点复制新颜色红色
                im.putpixel((x, y), (240, 0, 0))
            else:
                # 白色
                im.putpixel((x, y), (255, 255, 255))
                # 去除噪声
    # 转化灰度图
    im = im.convert('L')
    im_cv = np.array(im)
    blur = cv2.medianBlur(im_cv, 5)
    # 详细的轮廓数据
    contours = measure.find_contours(blur == 255, 0.5)
    # 轮廓最小外接矩形数据
    box_all = []
    for i in range(len(contours)):
        rect = cv2.minAreaRect(contours[i].astype(np.float32))
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        box_c = self.change_box(box)
        # print(box_c)
        x1, x2, y1, y2 = self.extract_box(box_c)
        if x2 - x1 >= 10 and y2 - y1 >= 10:
            box_all.append(box_c)
    # 在原始图像绘制检测边框
    # draw_img = cv2.drawContours(img_.copy(), box_all, -1, (0, 0, 255), 3)
    # cv2.imshow('draw_img', draw_img)
    # cv2.waitKey(0)
    return box_all
