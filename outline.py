# -*- coding:utf8 -*-
import os
from skimage import measure
import numpy as np
from PIL import Image
import cv2


class OutLine:
    def __init__(self):
        self.mask_path = 'data/mask'
        self.inpaint_path = 'data/inpaint'

    # 提取xy坐标
    def extract_box(self, box):
        x1 = np.min(box[:, 0])
        x2 = np.max(box[:, 0])
        y1 = np.min(box[:, 1])
        y2 = np.max(box[:, 1])
        return x1, x2, y1, y2

    # 改变x，y
    def change_box(self, box):
        box_list = box.tolist()
        box_change = []
        for item in box_list:
            box_change.append([item[1], item[0]])
        return np.array(box_change)

    # 单张轮廓坐标,以及外接矩形数据
    def box_data(self, path):
        img = Image.open(path)  # 打开图片
        im = img.convert('RGB')
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
        blur = cv2.medianBlur(im_cv, 5)
        dilate = cv2.dilate(blur, None, iterations=4)  # 膨胀
        erode = cv2.erode(dilate, None, iterations=3)  # 腐蚀
        # 开运算
        kernel = np.ones((5, 5), np.uint8)
        open = cv2.morphologyEx(erode, cv2.MORPH_OPEN, kernel)
        open = cv2.morphologyEx(open, cv2.MORPH_OPEN, kernel)
        # 轮廓数据
        _, contours, _ = cv2.findContours(open, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # 轮廓最小外接多边形数据
        box_all = []
        for cont in contours:
            # 取轮廓长度的0.012为epsilon 暂时最佳
            epsilon = 0.012 * cv2.arcLength(cont, True)
            epsilon_ = epsilon if epsilon <= 3 else 6
            # 预测多边形
            box = cv2.approxPolyDP(cont, epsilon_, True)
            # print(box)
            # print(box.shape)
            # img_re = cv2.polylines(img_, [box], True, (0, 0, 255), 2)
            box_all.append(box)
        # 在原始图像绘制检测边框
        # draw_img = cv2.drawContours(img_.copy(), box_all, -1, (0, 0, 255), 3)
        # cv2.imshow('draw_img', draw_img)
        # cv2.waitKey(0)
        return box_all

    # 去除文字和图标
    def inpaint(self, img_path, mask_path, inpaint_path):
        img = cv2.imread(img_path)
        mask = cv2.imread(mask_path, 0)
        # Alexandru Telea（INPAINT_TELEA） 方法更好用 7个像素暂时最佳
        dst1 = cv2.inpaint(img, mask, 7, cv2.INPAINT_TELEA)
        # cv2.imshow('dst1', dst1)
        cv2.imwrite(inpaint_path, dst1)

    # 提取边框信息
    def boxs(self, img_path, file_name):
        mask_path = self.change_mask_path(file_name)
        inpaint_path = self.change_inpaint_path(file_name)
        self.inpaint(img_path, mask_path, inpaint_path)
        box_all = self.box_data(inpaint_path)
        box_all = self.transform_box(box_all)
        return box_all

    # 转化格式box
    def transform_box(self, box):
        box_all = []
        for item in box:
            box_one = []
            x_min = np.min(item[:, :, 0])
            x_max = np.max(item[:, :, 0])
            y_min = np.min(item[:, :, 1])
            y_max = np.max(item[:, :, 1])
            x_distance = x_max - x_min
            y_distance = y_max - y_min
            if x_distance < 10 or y_distance < 10:
                continue
            for item_z in item:
                for item_y in item_z:
                    box_one.append(item_y)
            box_one = np.array(box_one)
            box_all.append(box_one)
        return box_all

    # 改变为mask的路径
    def change_mask_path(self, img_name):
        list_img = img_name.split('.')
        mask_path = self.mask_path + '/' + list_img[0] + '_mask.' + list_img[1]
        return mask_path

    # 改变为mask的路径
    def change_inpaint_path(self, img_name):
        list_img = img_name.split('.')
        inpaint_path = self.inpaint_path + '/' + list_img[0] + '_inpaint.' + list_img[1]
        return inpaint_path


if __name__ == '__main__':
    ol = OutLine()
    path = 'data/picture_merge/R000183C1_C00034AE0.png'
    box_all = ol.box_data(path)
