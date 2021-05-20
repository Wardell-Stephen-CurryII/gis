import cv2

img_path = 'data/icon/10-住宿服务.JPG'
img = cv2.imread(img_path)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

print(img)
print(gray)
# 高斯去噪
blurred = cv2.GaussianBlur(gray, (9, 9),0)
# 索比尔算子来计算x、y方向梯度
gradX = cv2.Sobel(blurred, ddepth=cv2.CV_32F, dx=1, dy=0)
gradY = cv2.Sobel(blurred, ddepth=cv2.CV_32F, dx=0, dy=1)

gradient = cv2.subtract(gradX, gradY)
gradient = cv2.convertScaleAbs(gradient)

cv2.imshow('img', img)
cv2.imshow('gray', gray)
cv2.imshow('blurred', blurred)
cv2.imshow('gradX', gradX)
cv2.imshow('gradY', gradY)
cv2.imshow('final', gradient)
cv2.waitKey()
# cv2.imwrite('data/result/blurred.jpg', blurred)