import argparse
import imutils
import datetime
import time
import cv2 as cv
import numpy as np
 
from imutils.video import VideoStream
from collections import deque
 
#Defining arguments to locate and play files
ap = argparse.ArgumentParser()
ap.add_argument("-v","--video",help="Path to the video file")
ap.add_argument("-b","--buffer",type=int,default=32,help="Max buffer size")
args = vars(ap.parse_args())
 
#Defining variables for the locations shown on frame
counter = 0
pts = deque(maxlen=args["buffer"])
 
green_lower = np.array([70, 40, 40])    # Lower boundary for green
green_upper = np.array([110, 255, 255])  # Upper boundary for green
red_lower = np.array([0, 100, 100], np.uint8)
red_upper = np.array([10, 255, 255], np.uint8)
 
 
 
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
    #blur = cv.GaussianBlur(hsv,(5,5),9)
    mask_green = cv.inRange(hsv, green_lower, green_upper)
    mask_green = cv.dilate(mask_green,None,iterations=2)
    mask_red = cv.inRange(hsv,red_lower,red_upper)
    mask_red = cv.dilate(mask_red,None,iterations=2)
 
    dst1 = cv.cornerHarris(mask_green,2,3,0.04)
    dst2 = cv.cornerHarris(mask_red,2,3,0.04)
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
     
 
    cv.imshow("Green",frame_w_corners_green)
    cv.imshow("Red",frame_w_corners_red)
 
    key = cv.waitKey(1) & 0xFF
 
    if key == ord("d"):
        break
 
if not args.get("video",False):
    v.stop()
 
else:
    v.release()
 
cv.destroyAllWindows()