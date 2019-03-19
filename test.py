import numpy as np
import cv2

img = cv2.imread("circle2.jpg")

n = 30

new_img = img[(np.tile(np.arange(0, n) * (img.shape[0]/n), n)).astype(int), (np.repeat(np.arange(0, n) * (img.shape[1]/n), n)).astype(int)]
new_img = new_img.reshape((n, n, 3))
new_img = (new_img > 220) * 255

cv2.imshow("", new_img.astype(np.uint8))
cv2.waitKey(0)