import cv2
import numpy as np
from PIL import Image
from skimage import measure

#行扫描，间隔k时，进行填充，填充值为1
def edge_connection(img, size, k):
    for i in range(size):
        Yi = np.where(img[i, :] > 0)
        if len(Yi[0]) >= 10: #可调整
            for j in range(0, len(Yi[0])-1):
                if Yi[0][j+1] - Yi[0][j] <= k:
                    img[i, Yi[0][j]:Yi[0][j+1]] = 1
    return img

# path = 'data/result/R000183C1_C00034AE0_inpaint.png'/
path = 'data/inpaint/R000183B3_C00034AD8_inpaint.png'
path_y = 'data/picture_merge/R000183B3_C00034AD8.png'
img_y = cv2.imread(path_y)
# print(img_y)
cv2.imshow('img_y', img_y)
cv2.waitKey(0)
# print(1)
img = Image.open(path_y)  # 打开图片
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
        if rgb[0] in range(205, 218) and rgb[1] in range(220, 231) and rgb[2] in range(236, 246):
            # 在各点复制新颜色黑色
            im.putpixel((x, y), (255, 255, 255))
        else:
            # 白色
            im.putpixel((x, y), (0, 0, 0))
# 转化灰度图
im = im.convert('L')
im_cv = np.array(im)
print(im_cv)
cv2.imshow('im_cv', im_cv)
cv2.waitKey(0)
gray = im_cv / 255.0 #像素值0-1之间
#sobel算子分别求出gx，gy
gx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
gy = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
mag, ang = cv2.cartToPolar(gx, gy, angleInDegrees=1) #得到梯度幅度和梯度角度阵列
g = np.zeros(gray.shape) #g与图片大小相同


#选取边缘，提取边缘坐标，将g中相应坐标像素值设为1
X, Y = np.where((mag > np.max(mag) * 0.3)&(ang >= 0)&(ang <= 90))
g[X, Y] = 1

#边缘连接，此过程只涉及水平，垂直边缘连接，不同角度边缘只需旋转相应角度即可
g = edge_connection(g, gray.shape[1], k=40)
g = cv2.rotate(g, 0)
g = edge_connection(g, gray.shape[0], k=40)
g = cv2.rotate(g, 2)

cv2.imshow("g", g)
cv2.waitKey(0)
# kernel = np.ones((5, 5), np.uint8)
# close = cv2.morphologyEx(im_cv, cv2.MORPH_CLOSE, kernel)
# cv2.imshow('close', close)
# cv2.waitKey(0)




