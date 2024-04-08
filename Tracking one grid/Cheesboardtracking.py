#Adjusting the code from the dots to use chessboard detection

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
 
green_lower = np.array([0,0,0], np.uint8)
green_upper = np.array([160, 255, 90], np.uint8)
 
#Defining variables for the locations shown on frame
counter = 0
pts = deque(maxlen=args["buffer"])
(dx,dy) = (0,0)
 
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
 
    #Working the frames to be able to locate and track dot
    frame = imutils.resize(frame,width=600)
    hsv = cv.cvtColor(frame,cv.COLOR_BGR2HSV)
    gray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
 
    mask = cv.inRange(hsv,green_lower,green_upper)
 
    found,corners = cv.findChessboardCorners(gray,(9,9))
 
    if found:
    # Reshape corners to have two elements per corner
        corners = corners.reshape(-1, 2)
     
        points = cv.drawChessboardCorners(mask,(9,9),corners,found)
 
        for i in range(len(corners)):
            pts.append(corners[i])
     
        #Setting counter and difference in locations between frames
        for j in np.arange(1,len(pts)):
            if pts[i-1] is None or pts[i] is None:
                continue
            if counter >= 10 and i==1 and pts[-10] is not None:
                dx = pts[-10][0] - pts[i][0]
                dy = pts[-10][1] - pts[i][1]
             
            thickness = int(np.sqrt(args["buffer"]/float(i+1))*2.5)
            cv.line(frame,pts[i-1],pts[i],(0,255,0),thickness)
 
        #Putting text on frame to show time, and movement from last frame
        cv.putText(frame,"dx:{},dy:{}".format(dx,dy),(10,frame.shape[0]-10),cv.FONT_HERSHEY_TRIPLEX,0.35,(0,255,0),1)
        cv.putText(frame,datetime.datetime.now().strftime("%A %d %B %Y %H:%M:%S%p"),(10,30),cv.FONT_HERSHEY_TRIPLEX,0.35,(0,255,0),1)
 
        #Saving frames to folder
        name = './VideoSave2/frame' + str(index) + '.jpg'
        cv.imwrite(name, frame)
        index+=1
 
        #Show frames and give option to exit
        cv.imshow("Frame",frame)
 
        key = cv.waitKey(1) & 0xFF
        counter += 1
 
        if key == ord("d"):
            break
    else:
        cv.imshow("Frame",mask)
 
        key = cv.waitKey(1) & 0xFF
        counter += 1
 
        if key == ord("d"):
            break
 
        print("Chessboard corners not found.")
     
     
if not args.get("video",False):
    v.stop()
 
else:
    v.release()
 
cv.destroyAllWindows()