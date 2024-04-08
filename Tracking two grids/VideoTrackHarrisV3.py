import argparse
import imutils
import datetime
import time
import cv2 as cv
import numpy as np
 
from imutils.video import VideoStream
from collections import deque
 
cv.namedWindow('Tracking')
def nothing(x):
    pass
 
#Defining arguments to locate and play files
ap = argparse.ArgumentParser()
ap.add_argument("-v","--video",help="Path to the video file")
ap.add_argument("-b","--buffer",type=int,default=32,help="Max buffer size")
args = vars(ap.parse_args())
 
#Defining upper and lower bounds to locate the dots
#Set trackbar to change value of red on frame
cv.createTrackbar("LH", "Tracking",
                   0, 255, nothing)
cv.createTrackbar("LS", "Tracking", 
                   0, 255, nothing)
cv.createTrackbar("LV", "Tracking", 
                   0, 255, nothing)
cv.createTrackbar("HH", "Tracking", 
                   0, 255, nothing)
cv.createTrackbar("HS", "Tracking", 
                   0, 255, nothing)
cv.createTrackbar("HV", "Tracking",
                   0, 255, nothing)
 
#Defining variables for the locations shown on frame
counter = 0
pts = deque(maxlen=args["buffer"])
 
green_lower = np.array([62, 57, 64])    # Lower boundary for green
green_upper = np.array([153, 255, 251])  # Upper boundary for green
#green_lower = np.array([35, 50, 50], dtype=np.uint8)
#green_upper = np.array([85, 255, 255], dtype=np.uint8)
red_lower = np.array([0, 87, 64], np.uint8)
red_upper = np.array([23, 255, 255], np.uint8)
 
 
 
#Reading files or use webcam to capture
if not args.get("video",False):
    v = imutils.video.VideoStream(src=0).start()
    frame_width = int(v.stream.get(cv.CAP_PROP_FRAME_WIDTH))
    frame_height = int(v.stream.get(cv.CAP_PROP_FRAME_HEIGHT))
else:
    v = cv.VideoCapture(args["video"])
    frame_width = int(v.get(cv.CAP_PROP_FRAME_WIDTH))
    frame_height = int(v.get(cv.CAP_PROP_FRAME_HEIGHT))
 
time.sleep(2.0)
 
index=0
 
file = open("./ResultsTwice/Gres.txt","w")
file2 = open("./ResultsTwice/Rres.txt","w")
 
 
while True:
    frame = v.read()
    if args.get("video", False):
        frame = frame[1]
    else:
        frame = frame
 
    if frame is None:
        break
 
    frame = imutils.resize(frame,width=600)
    gray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
    corners = cv.cornerHarris(gray,2,3,0.04)
 
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    blur = cv.GaussianBlur(hsv,(5,5),9)
 
    l_h = cv.getTrackbarPos("LH", "Tracking")
    l_s = cv.getTrackbarPos("LS", "Tracking")
    l_v = cv.getTrackbarPos("LV", "Tracking")
    h_h = cv.getTrackbarPos("HH", "Tracking")
    h_s = cv.getTrackbarPos("HS", "Tracking")
    h_v = cv.getTrackbarPos("HV", "Tracking")
    l_b = np.array([l_h, l_s, l_v])
    u_b = np.array([h_h, h_s, h_v])
 
    mask_green = cv.inRange(hsv, green_lower, green_upper)
    mask_green = cv.dilate(mask_green,None,iterations=2)
    mask_red = cv.inRange(hsv,red_lower,red_upper)
    mask_red = cv.dilate(mask_red,None,iterations=2)
 
    dst1 = cv.cornerHarris(mask_green,2,3,0.16)
    dst2 = cv.cornerHarris(mask_red,2,3,0.2)
    dst1 = cv.dilate(dst1,None)
    dst2 = cv.dilate(dst2,None)
    ret, dst1 = cv.threshold(dst1,0.01*dst1.max(),255,0)
    ret, dst2 = cv.threshold(dst2,0.01*dst2.max(),255,0)
    dst1 = np.uint8(dst1)
    dst2 = np.uint8(dst2)
  
    if ret:
        ret1,labels1, stats1, centroids1 = cv.connectedComponentsWithStats(dst1)
        ret2,labels2, stats2, centroids2 = cv.connectedComponentsWithStats(dst2)
        #Define the criteria to stop and refine the corners
        criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 100, 0.001)
        corners1 = cv.cornerSubPix(gray,np.float32(centroids1),(5,5),(-1,-1),criteria)
        corners2 = cv.cornerSubPix(gray,np.float32(centroids2),(5,5),(-1,-1),criteria)  
        #Drawing the corners
        res1 = np.hstack((centroids1,corners1))
        res2 = np.hstack((centroids2,corners2))
        res1 = np.int0(res1)
        res2 = np.int0(res2)
 
        frame_w_corners_red = frame.copy()
        frame_w_corners_green = frame.copy()
        frame_w_corners_green[res1[:,1],res1[:,0]]=[0,255,0]
        frame_w_corners_green[res1[:,3],res1[:,2]] = [0,255,0]
        frame_w_corners_red[res2[:,1],res2[:,0]]=[0,0,255]
        frame_w_corners_red[res2[:,3],res2[:,2]] = [0,0,255]
         
        #Saving files to folder
        for k in range(len(corners1)):
            res = print(corners1[k][0],",",corners1[k][1],file=file)
 
        for m in range(len(corners2)):
            res = print(corners2[m][0],",",corners2[m][1],file=file2)
  
    cv.imshow("Green",frame_w_corners_green)
    cv.imshow("Red",frame_w_corners_red)
    #cv.imshow("Green",mask_green)
    #cv.imshow("Red",mask_red)
    key = cv.waitKey(1) & 0xFF
 
    if key == ord("d"):
        break
 
if not args.get("video",False):
    v.stop()
 
else:
    v.release()
 
file.close()
file2.close()
 
cv.destroyAllWindows()