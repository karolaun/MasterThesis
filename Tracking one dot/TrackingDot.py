
#Import packages
from imutils.video import VideoStream
from collections import deque
import argparse
import datetime
import imutils
import time
import cv2 as cv
import numpy as np

#Defining some arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v","--video",help="path to the video file")
ap.add_argument("-b","--buffer",type=int,default=32,help="max buffer size")
args = vars(ap.parse_args())

#Defining upper and lower boundaries
upper = (64,255,255)
lower = (29,86,6)

#Setting variables
pts = deque(maxlen=args["buffer"])
counter = 0
(dx,dy) = (0,0)
direction = ""

#If video argument comes out as None, we read from webcam
if not args.get("video",False):
    vs = VideoStream(src=0).start()

#Otherwise we read from video file
else: 
    vs = cv.VideoCapture(args["video"])

res = cv.VideoWriter("output.avi",cv.VideoWriter_fourcc(*"MJPG"),10,(640,480))

time.sleep(2.0)

#Iterating through frames
while True:
    frame = vs.read()
    frame = frame[1] if args.get("video", False) else frame

    if frame is None:
        break

    #Work image to track wanted features
    frame = imutils.resize(frame,width=600)
    blurred = cv.GaussianBlur(frame,(11,11),0)
    hsv = cv.cvtColor(frame,cv.COLOR_BGR2HSV)

    #Mask to only detect the red
    mask = cv.inRange(hsv,lower,upper)
    mask = cv.erode(mask,None,iterations=2)
    mask = cv.dilate(mask,None,iterations=2)
    cv.imshow("mask",mask)

    #Finding contours of red circle
    contours = cv.findContours(mask.copy(),cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    center = None

    #If a circle exists, we draw circle around it, and track the center
    if len(contours)>0:
        c = max(contours,key=cv.contourArea)
        ((x,y),radius) = cv.minEnclosingCircle(c)
        M = cv.moments(c)
        center = (int(M["m10"]/M["m00"]),int(M["m01"]/M["m00"]))

        if radius > 10:
            cv.circle(frame,(int(x),int(y)),int(radius),(0,255,255),2)
            cv.circle(frame,center,5,(0,0,255),-1)
    pts.appendleft(center)

    #Calculate the movement of dot in both x- and y-direction
    for i in np.arange(1,len(pts)):
        if pts[i-1] is None or pts[i] is None:
            continue
        if counter >= 10 and i==1 and pts[-10] is not None:
            dx = pts[-10][0] - pts[i][0]
            dy = pts[-10][1] - pts[i][1]
            (dirX,dirY) = ("","")

            if np.abs(dx) > 20:
                dirX = "East" if np.sign(dx) == 1 else "West"
            if np.abs(dy) > 20:
                dirY = "North" if np.sign(dy) == 1 else "South"

            if dirX != "" and dirY != "":
                direction = "{}{}".format(dirY,dirX)
            else:
                direction = dirX if dirX != "" else dirY
        thickness = int(np.sqrt(args["buffer"]/float(i+1))*2.5)
        cv.line(frame,pts[i-1],pts[i],(0,0,255),thickness)

    #Write directions and times onto frame, did not always use the directions
    #cv.putText(frame,direction,(10,30),cv.FONT_HERSHEY_TRIPLEX,0.65,(0,0,255),3)
    cv.putText(frame,"dx:{},dy:{}".format(dx,dy),(10,frame.shape[0]-10),cv.FONT_HERSHEY_TRIPLEX,0.35,(0,0,255),1)
    cv.putText(frame,datetime.datetime.now().strftime("%A %d %B %Y %H:%M:%S%p"),(10,30),cv.FONT_HERSHEY_TRIPLEX,0.35,(0,0,255),1)

    res.write(frame)
    cv.imshow("Frame",frame)
    
    key = cv.waitKey(1) & 0xFF 
    counter += 1

    if key == ord("d"):
        break

if not args.get("video",False):
    vs.stop()

else:
    vs.release()

res.release()

cv.destroyAllWindows()

