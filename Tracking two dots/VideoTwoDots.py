#Disclaimer:
#This code is greatly inspired by the code written by Adrian Rosebrock here: https://pyimagesearch.com/2015/09/21/opencv-track-object-movement/

#Packages
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
 
#Defining upper and lower bounds to locate the dots
red_lower = np.array([136, 87, 111], np.uint8)
red_upper = np.array([180, 255, 255], np.uint8)
green_lower = np.array([25, 52, 72], np.uint8)
green_upper = np.array([102, 255, 255], np.uint8)
blue_lower = np.array([94, 80, 2], np.uint8)
blue_upper = np.array([120, 255, 255], np.uint8)
 
#Defining variables for the locations shown on frame
counter = 0
counter1= 0
pts1 = deque(maxlen=args["buffer"])
pts2 = deque(maxlen=args["buffer"])
(dx,dy) = (0,0)
(dx_r,dy_r) = (0,0)
 
 
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
 
#While loop to go through frames and track
while True:
    frame = v.read()
    if args.get("video", False):
        frame = frame[1]
    else:
        frame = frame
 
    if frame is None:
        break
 
    #Working the frames to be able to locate and track red dot
    frame = imutils.resize(frame,width=600)
    blur = cv.GaussianBlur(frame,(11,11),4)
    hsv = cv.cvtColor(blur,cv.COLOR_BGR2HSV)
 
    canny = cv.Canny(hsv,125,175)
    #cv.imshow("Canny",canny)
    #Making a mask
    mask1 = cv.inRange(hsv,green_lower,green_upper)
    mask1 = cv.erode(mask1,None,iterations=2)
    mask1 = cv.dilate(mask1,None,iterations=2)
    mask2 = cv.inRange(hsv,red_lower,red_upper)
    mask2 = cv.erode(mask2,None,iterations=2)
    mask2 = cv.dilate(mask2,None,iterations=2)
    cv.imshow("mask",mask1)
    cv.imshow("mask1",mask2)
 
    contours1 = cv.findContours(mask1.copy(),cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
    contours1 = imutils.grab_contours(contours1)
    contours2 = cv.findContours(mask2.copy(),cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
    contours2 = imutils.grab_contours(contours2)
    center1 = None
    center2 = None
 
    #Making circle and track
    if len(contours1)>0:
        c1 = max(contours1,key=cv.contourArea)
        ((x,y),radius) = cv.minEnclosingCircle(c1)
        M1 = cv.moments(c1)
        center1 = (int(M1["m10"]/M1["m00"]),int(M1["m01"]/M1["m00"]))
 
        if radius > 10:
            cv.circle(frame,(int(x),int(y)),int(radius),(0,255,255),2)
            cv.circle(frame,center1,5,(0,0,255),-1)
    pts1.appendleft(center1)
 
    if len(contours2)>0:
        c2 = max(contours2,key=cv.contourArea)
        ((x1,y1),radius1) = cv.minEnclosingCircle(c2)
        M = cv.moments(c2)
        center2 = (int(M["m10"]/M["m00"]),int(M["m01"]/M["m00"]))
 
        if radius1 > 10:
            cv.circle(frame,(int(x1),int(y1)),int(radius1),(0,255,255),2)
            cv.circle(frame,center2,5,(0,0,255),-1)
    pts2.appendleft(center2)
 
    #Setting counter and difference in locations between frames
    for i in np.arange(1,len(pts1)):
        if pts1[i-1] is None or pts1[i] is None:
            continue
        if counter >= 10 and i==1 and pts1[-10] is not None:
            dx = pts1[-10][0] - pts1[i][0]
            dy = pts1[-10][1] - pts1[i][1]
             
        thickness = int(np.sqrt(args["buffer"]/float(i+1))*2.5)
        cv.line(frame,pts1[i-1],pts1[i],(0,255,0),thickness)
 
    if len(pts2) >= 10:
        if None not in pts2:
            dx_r = pts2[-1][0] - pts2[0][0]
            dy_r = pts2[-1][1] - pts2[0][1]
         
        for l in range(1, len(pts2)):
            thickness2 = int(np.sqrt(args["buffer"] / float(len(pts2)))*2.5)
            if pts2[l-1] is not None and pts2[l] is not None:
                cv.line(frame, pts2[l-1], pts2[l], (0, 0, 255), thickness2)
 
    cv.putText(frame,"dx_red:{},dy_red:{}".format(dx_r,dy_r),(10,frame.shape[0]-20),cv.FONT_HERSHEY_TRIPLEX,0.35,(0,255,0),1)
    cv.putText(frame,"dx_green:{},dy_green:{}".format(dx,dy),(10,frame.shape[0]-10),cv.FONT_HERSHEY_TRIPLEX,0.35,(0,255,0),1)
    cv.putText(frame,datetime.datetime.now().strftime("%A %d %B %Y %H:%M:%S%p"),(10,30),cv.FONT_HERSHEY_TRIPLEX,0.35,(0,255,0),1)
 
    name = './Videosaved/frame' + str(index) + '.jpg'
    cv.imwrite(name, frame)
    index+=1
 
    # next frame
    index += 1
    cv.imshow("Frame",frame)
 
    key = cv.waitKey(1) & 0xFF
    counter += 1
 
    if key == ord("d"):
        break
 
if not args.get("video",False):
    v.stop()
 
else:
    v.release()
 
cv.destroyAllWindows()