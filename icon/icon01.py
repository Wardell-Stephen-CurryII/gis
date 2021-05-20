import cv2
import numpy as np


def flann_match_icon_once(img1, img2, icon_name):
    # 使用SIFT算法获取图像特征的关键点和描述符
    # sift = cv2.xfeatures2d.SIFT_create()
    sift = cv2.xfeatures2d.SURT_create()
    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)
    print(des1)
    print(des2)

    # 定义FLANN匹配器
    indexParams = dict(algorithm=0, trees=10)
    searchParams = dict(checks=50)
    flann = cv2.FlannBasedMatcher(indexParams, searchParams)
    # 使用KNN算法实现图像匹配，并对匹配结果排序
    # matches=flann.knnMatch(des1,des2,k=2)
    matches = flann.knnMatch(np.asarray(des1, np.float32), np.asarray(des2, np.float32), k=2)
    matches = sorted(matches, key=lambda x: x[0].distance)
    print(matches)
    # print(len(matches))

    # 去除错误匹配，0.5是系数，系数大小不同，匹配的结果也不同
    goodMatches = []
    for m, n in matches:
        # print(m.distance)
        # print(n.distance)
        if m.distance < 0.5 * n.distance:
            goodMatches.append(m)
    print(goodMatches)

    # 获取某个点的坐标位置
    # index是获取匹配结果的中位数
    # index=int(len(goodMatches)/2)
    result = []
    for index in range(len(goodMatches)):
        # queryIdx是目标图像的描述符索引
        # print(kp1[goodMatches[index].queryIdx].pt)
        x, y = kp1[goodMatches[index].queryIdx].pt
        # 将坐标位置勾画在img1图片上，并显示
        cv2.rectangle(img1, (int(x), int(y)), (int(x), int(y)), (0, 255, 0), 2)
        # print(x)
        # print(y)
        result.append([int(x), int(y), icon_name])
    # cv2.imwrite('data/result/{}.jpg'.format(icon_name), img1)
    # cv2.imshow('通行设备',img1)
    # cv2.waitKey()
    return result


def match_icon_more(img1):
    icon_list = ['专卖店', '中国工商银行', '交通银行', '住宅区', '住宿服务', '便民商店', '停车场', '公共厕所', '公检法机构', '医疗保健服务', '医药保健销售店', '图书馆',
                 '地铁站', '学校', '学校内部设施', '平安银行', '幼儿园', '政府机关', '楼宇', '科教文化服务', '科研机构', '篮球场馆', '美容美发店', '足球场', '运动场馆',
                 '通行设施', '风景名胜', '餐饮服务', '餐饮服务_', '高等院校']
    x_y_type = []
    for item in icon_list:
        print(item)
        img_icon_path = 'data/icon/{}.png'.format(item)
        img_icon = cv2.imread(img_icon_path)
        xy = flann_match_icon_once(img1, img_icon, item)
        print(xy)
        x_y_type += xy
    print(x_y_type)


if __name__ == '__main__':
    tile_path = 'data/tile/R000183B1/C00034ACE.png'
    print(tile_path)
    img1 = cv2.imread(tile_path)
    img2 = cv2.imread('data/icon/住宅区.png')
    # cv2.imshow('住宿服务', img1)
    # cv2.imshow('住宿服务1', img2)
    # cv2.waitKey()
    xy = flann_match_icon_once(img1, img2, '住宅区')
    print(xy)
    # match_icon_more(img1)
