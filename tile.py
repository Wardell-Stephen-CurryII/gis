#!/usr/bin/env python
# coding: utf-8

import cv2
import numpy as np
from icon.icon03 import Icon
from ocr_tile import BaiDuOcr
from outline import OutLine
import math
from PIL import Image


# 瓦片
class Tile:
    def __init__(self):
        self.icon = Icon()
        self.bdocr = BaiDuOcr()
        self.ol = OutLine()



    # 定位瓦片文字位置
    def picture_detection(self, img_path,img_name):
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
        # 转换灰度并去噪声
        gray = cv2.cvtColor(img_, cv2.COLOR_BGR2GRAY)
        # 提取图像的梯度
        # 以Sobel算子计算x，y方向上的梯度，之后在x方向上减去y方向上的梯度，通过这个减法，留下具有高水平梯度和低垂直梯度的图像区域
        gradX = cv2.Sobel(gray, ddepth=cv2.CV_32F, dx=1, dy=0)
        gradY = cv2.Sobel(gray, ddepth=cv2.CV_32F, dx=0, dy=1)
        gradient = cv2.subtract(gradX, gradY)
        gradient = cv2.convertScaleAbs(gradient)
        # 高斯滤波
        blurred = cv2.GaussianBlur(gradient, (9, 9), 0)
        (_, thresh) = cv2.threshold(blurred, 90, 255, cv2.THRESH_BINARY)
        # # 建立一个椭圆核函数
        # kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (25, 25))
        # 执行图像形态学
        closed = cv2.dilate(thresh, None, iterations=4) # 膨胀
        closed = cv2.erode(closed, None, iterations=6)  # 腐蚀
        closed = cv2.dilate(closed, None, iterations=3)
        closed_mask = cv2.dilate(closed, None, iterations=2)
        mask_path = self.ol.change_mask_path(img_name)
        # 使用mask更好用（也就是closed111）
        cv2.imwrite(mask_path, closed_mask)
        (img_01, cnts, hierarchy) = cv2.findContours(closed.copy(),
                                                     cv2.RETR_LIST,
                                                     cv2.CHAIN_APPROX_SIMPLE)
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
        # draw_img = cv2.drawContours(img_.copy(), box_gather, -1, (0, 0, 255), 3)
        # cv2.imshow('draw_img', draw_img)
        # cv2.waitKey(0)
        # cv2.imwrite(save_path,draw_img)
        return box_gather

    # 切割图片-图标识别-文字识别-识别区域；匹配对应
    def picture_recognition_once(self, img_path, box_gather, save_path):
        # 文字
        file_name_h = img_path.split('/')[-1]
        file_name = file_name_h.split('.')[0]
        row_index, col_index = file_name.split('_')
        # 文字信息
        word_detail = []
        img = cv2.imread(img_path)
        # 区域
        box_all = self.ol.boxs(img_path,file_name_h)
        # 图标
        icon_data = self.icon.choice_centre(img)
        icon_index_list = []
        if len(box_gather) != 0:
            # 匹配有文字和图标和区域数据
            for j in range(len(box_gather)):
                # 裁剪图片
                xs = [i[0] for i in box_gather[j]]
                ys = [i[1] for i in box_gather[j]]
                x1 = abs(min(xs))
                x2 = abs(max(xs))
                y1 = abs(min(ys))
                y2 = abs(max(ys))
                hight = y2 - y1
                width = x2 - x1
                crop_img = img[y1 - 3:y1 + 3 + hight, x1 - 3:x1 + width + 3]
                word_x = (x1 + width / 2)
                word_y = (y1 + hight / 2)
                if 255 < word_x <= 511 and 255 < word_y <= 511:
                    savepath = (save_path + '/' + file_name + '_%d.png') % j
                    # print(savepath)
                    cv2.imwrite(savepath, crop_img)
                    words = self.bdocr.merge_word(savepath)
                    if words != '':
                        box = self.match_word_outline(word_x, word_y,row_index,col_index, box_all)
                        if box:
                            box_str = str(box)
                        else:
                            box_str = None
                        icon_x, icon_y, icon_name, icon_code, icon_index = self.match_word_icon(word_x, word_y,
                                                                                                icon_data)
                        if icon_index is not None:
                            icon_index_list.append(icon_index)
                        word_x_sql, word_y_sql, row_256_word, col_256_word = self.character_poixy(
                                        word_x, word_y,row_index,col_index)
                        icon_x_sql, icon_y_sql, row_256_icon, col_256_icon = self.character_poixy(
                                        icon_x, icon_y,row_index, col_index)
                        one = [savepath, word_x, word_y, icon_x, icon_y, icon_name, icon_code, row_index, col_index,
                               words,box_str,word_x_sql, word_y_sql, row_256_word, col_256_word, icon_x_sql, icon_y_sql,
                               row_256_icon,col_256_icon]
                        print(one)
                        word_detail.append(one)
        # 加入只有图标的数据
        for i in range(len(icon_data)):
            if i not in icon_index_list:
                icon_x_, icon_y_, icon_name_, icon_code_ = icon_data[i]
                icon_x_sql_, icon_y_sql_, row_256_icon_, col_256_icon_ = self.character_poixy(
                            icon_x_, icon_y_, row_index, col_index)
                one = [None, None, None, icon_x_, icon_y_, icon_name_, icon_code_, row_index, col_index, None, None,
                        None, None, None, None,icon_x_sql_, icon_y_sql_, row_256_icon_, col_256_icon_]
                word_detail.append(one)
        print(word_detail)
        return word_detail

    # 匹配文字和区域
    def match_word_outline(self, word_x, word_y,row_index,col_index, box_all):
        for i in range(len(box_all)):
            box = box_all[i]
            x1, x2, y1, y2 = self.extract_box(box)
            if x1 <= word_x <= x2 and y1 <= word_y <= y2:
                # outline = [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]
                outline = box
                poi_outline = []
                for item in outline:
                    poi_x, poi_y ,poi_r, poi_c = self.character_poixy(item[0],item[1],row_index,col_index)
                    dot = (poi_c+'_'+str(poi_x),poi_r+'_'+str(poi_y))
                    poi_outline.append(dot)
                return poi_outline

    # 匹配文字和图标
    def match_word_icon(slef, word_x, word_y, icon_data):
        if len(icon_data) == 0:
            return None, None, None, None, None
        for i in range(len(icon_data)):
            icon_x = icon_data[i][0]
            icon_y = icon_data[i][1]
            icon_name = icon_data[i][2]
            icon_code = icon_data[i][3]
            # 欧式距离
            ueclidean_distance = math.sqrt((icon_x - word_x) ** 2 + (word_y - icon_y) ** 2)
            # 阈值25像素
            if ueclidean_distance <= 25:
                return icon_x, icon_y, icon_name, icon_code, i
        return None, None, None, None, None

    # 九宫格中心点坐标行x,y
    # 文字中心(会有跨图片问题)
    def character_poixy(self, x, y, row_index, col_index):
        if not row_index or not col_index or x is None or y is None:
            return None, None, None, None
        row = row_index[4:]
        col = col_index[4:9]
        row_1 = ('R000' + hex(int(row, 16) - 1)[2:]).upper()
        col_1 = ('C000' + hex(int(col, 16) - 1)[2:]).upper()
        row_11 = ('R000' + hex(int(row, 16) + 1)[2:]).upper()
        col_11 = ('C000' + hex(int(col, 16) + 1)[2:]).upper()

        # 当前中心点
        if x < 255:
            if y < 255:
                row_256 = row_1
                col_256 = col_1
                x = x
                y = y
            elif y < 511:
                row_256 = row_index[:9]
                col_256 = col_1
                x = x
                y = y - 255
            else:
                row_256 = row_11
                col_256 = col_1
                x = x
                y = y - 511
        elif x < 511:
            if y < 255:
                row_256 = row_1
                col_256 = col_index[:9]
                x = x - 255
                y = y
            elif y < 511:
                row_256 = row_index[:9]
                col_256 = col_index[:9]
                x = x - 255
                y = y - 255
            else:
                row_256 = row_11
                col_256 = col_index[:9]
                x = x - 255
                y = y - 511
        else:
            if y < 255:
                row_256 = row_1
                col_256 = col_11
                x = x - 511
                y = y
            elif y < 511:
                row_256 = row_index[:9]
                col_256 = col_11
                x = x - 511
                y = y - 255
            else:
                row_256 = row_11
                col_256 = col_11
                x = x - 511
                y = y - 511
        return x, y, row_256, col_256

    # 提取xy坐标
    def extract_box(self,box):
        x1 = np.min(box[:, 0])
        x2 = np.max(box[:, 0])
        y1 = np.min(box[:, 1])
        y2 = np.max(box[:, 1])
        return x1, x2, y1, y2

    # 去重数据
    def remove_duplication(self, tile_data):
        remove_tile_data = []
        for item in tile_data:
            # word_x = item[1]
            # word_y = item[2]
            icon_x = item[3]
            words_str = item[9]
            if icon_x != None or words_str != '':
                remove_tile_data.append(item)
        return remove_tile_data


if __name__ == '__main__':
    tile = Tile()
    # tile.main()
