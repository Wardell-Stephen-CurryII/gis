import numpy as np
import cv2 as cv

img = cv.imread('data/picture_merge/R000183C1_C00034AE0.png')
mask = cv.imread('data/result/R000183C1_C00034AE0_mask3.png', 0)
# Alexandru Telea（INPAINT_TELEA） 方法更好用 7个像素暂时最佳
dst1 = cv.inpaint(img, mask, 7, cv.INPAINT_TELEA)
# dst2 = cv.inpaint(img,mask,5,cv.INPAINT_NS)
cv.imshow('dst1', dst1)
# cv.imshow('dst2',dst2)
cv.imwrite('data/result/R000183C1_C00034AE0_inpaint3.png', dst1)
# cv.imwrite('data/result/R000183BA_C00034AD9_inpaint4.png', dst2)
# cv.waitKey(0)
# cv.destroyAllWindows()
