#Packages
import argparse
import imutils
import datetime
import time
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
 
from imutils.video import VideoStream
from collections import deque
import imutils
 
#Defining arguments to locate and play files
ap = argparse.ArgumentParser()
ap.add_argument("-v","--video",help="Path to the video file")
ap.add_argument("-b","--buffer",type=int,default=32,help="Max buffer size")
args = vars(ap.parse_args())
 
counter = 0
pts1 = deque(maxlen=args["buffer"])
pts2 = deque(maxlen=args["buffer"])
 
 
green_lower = np.array([50, 40, 40])    # Lower boundary for green
green_upper = np.array([90, 255, 255])  # Upper boundary for green
#green_lower = np.array([35, 50, 50], dtype=np.uint8)
#green_upper = np.array([85, 255, 255], dtype=np.uint8)
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
 
index=0
 
while True:
    frame = v.read()
    if args.get("video", False):
        frame = frame[1]
    else:
        frame = frame
 
    if frame is None:
        break
 
    #Working the frames to be able to locate and track red dot
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    blur = cv.GaussianBlur(hsv,(5,5),6)
    mask_green = cv.inRange(blur, green_lower, green_upper)
    mask_green = cv.dilate(mask_green,None,iterations=2)
    mask_red = cv.inRange(blur,red_lower,red_upper)
    mask_red = cv.dilate(mask_red,None,iterations=2)
 
    cv.imshow("Red",mask_red)
    #plt.show()
    cv.imshow("Green",mask_green)
    #plt.show()
 
    contours1, _ = cv.findContours(mask_green.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    contours2, _ = cv.findContours(mask_red.copy(),cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
 
     
 
    for contour in contours1:
        x = [point[0][0] for point in contour]  # Extract x coordinates from each point in the contour
        y = [point[0][1] for point in contour]  # Extract y coordinates from each point in the contour
        #plt.plot(x, y,"o", color="green",markersize=0.5) # Plot the contour
 
    # Plot contours from contours2
    for contour in contours2:
        x = [point[0][0] for point in contour]  # Extract x coordinates from each point in the contour
        y = [point[0][1] for point in contour]  # Extract y coordinates from each point in the contour
        #plt.plot(x, y,"o", color="red",markersize=0.5)  # Plot the contour
    # Set plot labels and title
    #plt.xlabel('X-axis')
    #plt.ylabel('Y-axis')
    #plt.title('Contours Plot')
 
    # Show the plot
    #plt.grid(True)
    #plt.gca().invert_yaxis()  # Invert y-axis to match the image coordinates
    #plt.show()
    for m in range(len(contours1)):
        results = './ResultsTwoGrids/resc1_' + str(m) + '.csv'
        if index==1:
            file2 = open(results,"w")
        file2 = open(results,"a")
        print(contours1[m][0],",",contours1[m][1],file=file2)
        file2.close()
 
    for n in range(len(contours2)):
        results = './ResultsTwoGrids/res' + str(n) + '.csv'
        if index==1:
            file2 = open(results,"w")
        file2 = open(results,"a")
        print(contours2[n][0],",",contours2[n][1],file=file2)
        file2.close()
 
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