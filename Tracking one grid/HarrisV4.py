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
 
#Defining variables for the locations shown on frame
counter = 0
pts = deque(maxlen=args["buffer"])
 
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
 
file = open("res.txt","w")
 
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
    gray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
     
    dst = cv.cornerHarris(gray,2,3,0.07)
    dst = cv.dilate(dst,None)
    ret, dst = cv.threshold(dst,0.01*dst.max(),255,0)
    dst = np.uint8(dst)
    cv.imshow("dst",dst)
 
    if ret:
        ret,labels, stats, centroids = cv.connectedComponentsWithStats(dst)
        #Define the criteria to stop and refine the corners
        criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 100, 0.001)
        corners = cv.cornerSubPix(gray,np.float32(centroids),(50,50),(-1,-1),criteria)    
        #Drawing the corners
        res = np.hstack((centroids,corners))
        res = np.int0(res)
        frame[res[:,1],res[:,0]]=[0,0,255]
        frame[res[:,3],res[:,2]] = [0,255,0]
 
        #Setting counter and difference in locations between frames
        for j in np.arange(1,len(pts)):
            if pts[j-1] is None or pts[j] is None:
                continue
             
            thickness = int(np.sqrt(args["buffer"]/float(j+1))*2.5)
            cv.line(frame,pts[j-1],pts[j],(0,255,0),thickness)
 
        #Putting text on frame to show time, and movement from last frame
        cv.putText(frame,datetime.datetime.now().strftime("%A %d %B %Y %H:%M:%S%p"),(10,30),cv.FONT_HERSHEY_TRIPLEX,0.35,(0,255,0),1)
 
        #Saving frames to folder
        name = './VideoSave2/frame' + str(index) + '.jpg'
        cv.imwrite(name, frame)
        threshimg = "./Thresh/frame" + str(index) + ".jpg"
        cv.imwrite(threshimg,dst)
        index+=1
 
        #Show frames and give option to exit
        cv.imshow("Frame",frame)
 
        for k in range(len(corners)):
            res = print(corners[k][0],",",corners[k][1],file=file)
 
        #Saving files to folder
        for m in range(len(corners)):
            results = './Results/restest' + str(m) + '.txt'
            if index == 1:
                file2 = open(results, "w")
                print(corners[m][0], ",", corners[m][1], file=file2)   
            else:
                file2 = open(results, "a")
 
                # Open the file to read the last line
                file2 = open(results, "r")
                lines = file2.readlines()
                file2.close()
 
                if len(lines) > 0:
                    prev_line = lines[-1].strip()
                    prev_value1,prev_value2 = prev_line.split(",")
                    prev_value1 = float(prev_value1)
                    prev_value2 = float(prev_value2)
 
                    # Define the limit
                    limit = float(50) # Adjust this as needed
 
                    # Check if the current corner's coordinates are within the limit of the previous coordinates
                    if (abs(corners[m][0] - prev_value1) <= limit) and (abs(corners[m][1] - prev_value2) <= limit):
                        print("Both current values are within the limit.")
                        # Open the file to append the current corner's coordinates
                        file2 = open(results, "a")
                        print(corners[m][0], ",", corners[m][1], file=file2)
                        file2.close()
                    else:
                        print("Values are not within limits")
                else:
                    print("First corner detected. No comparison made.")
 
        # Close the file after the loop finishes
        if file2:
            file2.close()
 
        key = cv.waitKey(1) & 0xFF
        counter += 1
 
        if key == ord("d"):
            break
    else:
        key = cv.waitKey(1) & 0xFF
        counter += 1
 
        if key == ord("d"):
            break
 
        print("Corners not found.")
     
if not args.get("video",False):
    v.stop()
 
else:
    v.release()
 
file.close()
 
cv.destroyAllWindows()