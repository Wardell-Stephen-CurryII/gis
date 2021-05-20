# opencv----多目标匹配
import cv2
import numpy
import os


class Icon(object):
    def __init__(self):
        self.tiles_path = '../data/tile/L18'
        self.icon_list = [('专卖店', '061200'), ('中国光大银行', '160113'), ('中国工商银行', '160105'), ('中国建设银行', '160106'),
                          ('中国民生银行', '160112'), ('中国邮政储蓄银行', '160139'), ('中国银行', '160104'), ('交通银行', '160108'),
                          ('休闲场所', '080500'), ('住宅区', '120300'), ('住宿服务', '100000'), ('便民商店', '060200'),
                          ('停车场', '150900'), ('公交车站', '150700'), ('公共厕所', '200300'), ('公园广场', '110100'),
                          ('公安警察', '130501'), ('公检法机构', '130500'), ('北京银行', '160119'), ('医疗保健服务', '090000'),
                          ('医药保健销售店', '090600'), ('商场', '060100'), ('图书馆', '140500'), ('地铁站', '150500'),
                          ('娱乐场所', '080300'), ('学校', '141200'), ('学校内部设施', '141207'), ('寺庙道观', '110205'),
                          ('幼儿园', '141204'), ('影剧院', '080600'), ('招商银行', '160109'), ('摄影冲印店', '071300'),
                          ('政府机关', '130100'), ('楼宇', '120200'), ('汽车服务', '010000'), ('汽车维修', '030000'),
                          ('洗衣店', '071500'), ('科教文化服务', '140000'), ('科研机构', '141300'), ('篮球场馆', '080104'),
                          ('综合医院', '090100'), ('综合市场', '060700'), ('美容美发店', '071100'), ('足球场', '080105'),
                          ('运动场馆', '080100'), ('通行设施', '990000'), ('邮局', '070400'), ('银行', '160100'),
                          ('风景名胜', '110200'), ('餐饮服务', '050000'), ('餐饮服务_', '050000'), ('高等院校', '050000')]

    # 单瓦片单图片多匹配
    def flann_match_icon_once(self, target, template, icon_name, icon_code):
        # icon_name = '楼宇'
        loc_label = []
        # 获得模板图片的高宽尺寸
        theight, twidth = template.shape[:2]
        # target = cv2.cvtColor(target, cv2.COLOR_BGR2RGB)
        # 执行模板匹配，采用的匹配方式cv2.TM_SQDIFF_NORMED
        try:
            result = cv2.matchTemplate(target, template, cv2.TM_SQDIFF_NORMED)
        except:
            return loc_label
        # 归一化处理
        # cv2.normalize( result, result, 0, 1, cv2.NORM_MINMAX, -1 )
        # 寻找矩阵（一维数组当做向量，用Mat定义）中的最大值和最小值的匹配结果及其位置
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        # print('匹配结果吻合度：')
        # print(min_val)
        # print('匹配结果位置：')
        # print(min_loc)
        # 对于cv2.TM_SQDIFF及cv2.TM_SQDIFF_NORMED方法min_val越趋近与0匹配度越好，匹配位置取min_loc,对于其他方法min_val越趋近于1匹配度越好，匹配位置取max_loc
        # strmin_val = str(min_val)
        numOfloc = 0
        # 第一次筛选----规定匹配阈值，将满足阈值的从result中提取出来
        # 对于cv2.TM_SQDIFF及cv2.TM_SQDIFF_NORMED方法设置匹配阈值为0.01
        # print(result)
        threshold = 0.01
        loc = numpy.where(result < threshold)
        # print(loc[::-1])
        # 遍历提取出来的其他的位置
        for other_loc in zip(*loc[::-1]):
            # print(other_loc)
            numOfloc = numOfloc + 1
            # cv2.rectangle(target, other_loc, (other_loc[0] + twidth, other_loc[1] + theight), (0, 0, 225), 2)
            loc_label.append([int(other_loc[0] + twidth / 2), int(other_loc[1] + theight / 2), icon_name, icon_code])
        # if numOfloc != 0:
        #     str_numOfloc = str(numOfloc)
        #     cv2.imshow(str_numOfloc, target)
        #     cv2.waitKey(0)
        # print('匹配数量为' + str_numOfloc)
        # print(loc_label)
        return loc_label

    # 筛选中心图的图标
    def choice_centre(self,target):
        icon_data_ = []
        icon_data = self.match_icon_more(target)
        for i in range(len(icon_data)-1,-1,-1):
            x = icon_data[i][0]
            y = icon_data[i][1]
            if 255 < x <= 511 and 255 < y <= 511:
                icon_data_.append(icon_data[i])
        return icon_data_


    # 单瓦片多图标匹配
    def match_icon_more(self, target):
        x_y_type = []
        for item in self.icon_list:
            # print(item)
            img_icon_path = 'data/icon/{}.png'.format(item[0])
            img_icon = cv2.imread(img_icon_path)
            # print(img_icon)
            xy = self.flann_match_icon_once(target, img_icon, item[0], item[1])
            # print(xy)
            x_y_type += xy
        # print('单瓦片结果为：')
        # print(x_y_type)
        return x_y_type

    # 遍历解析所有瓦片
    def main(self):
        for curdir, subdirs, files in os.walk(self.tiles_path):
            for png in (file for file in files if file.endswith('.png')):
                # print(png)
                tile_path = os.path.join(curdir, png)
                print(tile_path)
                target = cv2.imread(tile_path)
                x_y_type = self.match_icon_more(target)


if __name__ == '__main__':
    path = '/Users/linxiaohai/资料/gis/gis_icon/data/picture_merge_3/R000183B2_C00034AD1.png'
    target = cv2.imread(path)
    icon = Icon()
    icon.match_icon_more(target)
