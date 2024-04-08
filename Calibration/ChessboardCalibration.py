import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
 
img = cv.imread("IMG-5386.jpg")
gray = cv.cvtColor(img,cv.COLOR_BGR2RGB)
 
found,corners = cv.findChessboardCorners(img,(5,9))
corners= corners.reshape(-1,2)
cv.drawChessboardCorners(gray,(9,9),corners,found)
plt.imshow(gray)