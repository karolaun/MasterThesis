#Import packages
from imutils.video import VideoStream
import numpy as np
import cv2
import time
import imutils
import argparse

cv2.namedWindow("Trackbar")
def nothing(x):
    pass

ap = argparse.ArgumentParser()
ap.add_argument("-v","--video",help="Path to the video file")
ap.add_argument("-b","--buffer",type=int,default=32,help="Max buffer size")
args = vars(ap.parse_args())

cv2.createTrackbar("LH","Trackbar",
                  0,255,nothing)
cv2.createTrackbar("LS","Trackbar",
                  0,255,nothing)
cv2.createTrackbar("LV","Trackbar",
                  0,255,nothing)
cv2.createTrackbar("HH","Trackbar",
                  0,255,nothing)
cv2.createTrackbar("HS","Trackbar",
                  0,255,nothing)
cv2.createTrackbar("HV","Trackbar",
                  0,255,nothing)



if not args.get("video",False):
    v = VideoStream(src=0).start()
    time.sleep(2.0)
else:
    v = cv2.VideoCapture(args["video"])
    frame_width = int(v.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(v.get(cv2.CAP_PROP_FRAME_HEIGHT))
    time.sleep(2.0)

#Works for well lit conditions
#green_lower = np.array([20, 63, 15],np.uint8)   
#green_upper = np.array([79, 255, 240],np.uint8)  
#red_lower = np.array([0, 164, 174], np.uint8) 
#red_upper = np.array([216, 255, 255], np.uint8) 
red_lower = np.array([0,113,81],np.uint8)
red_upper = np.array([74,255,255],np.uint8)
green_lower = np.array([45,75,47],np.uint8)
green_upper = np.array([147,255,255],np.uint8)


index=0
paused=False

#Add filepath if needed

while True:
    #Collecting frames
    if not paused:
        #To be able to pause video at a frame before moving to next
        ret, frame = v.read()
        
        if not ret:
            print("End of video")
            break

    frame = imutils.resize(frame,width=600)
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    #Working image to better track
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    blur = cv2.GaussianBlur(hsv,(5,5),6)

    #Collecting trackbar values
    lh = cv2.getTrackbarPos("LH","Trackbar")
    ls = cv2.getTrackbarPos("LS","Trackbar")
    lv = cv2.getTrackbarPos("LV","Trackbar")
    hh = cv2.getTrackbarPos("HH","Trackbar")
    hs = cv2.getTrackbarPos("HS","Trackbar")
    hv = cv2.getTrackbarPos("HV","Trackbar")
    lb = np.array([lh,ls,lv])
    ub = np.array([hh,hs,hv])

    #Creating masks to detect colours
    #Using lb and ub to adjust with trackbar and boundaries if satisfied with colours
    mask_green = cv2.inRange(hsv,green_lower,green_upper)
    mask_green = cv2.dilate(mask_green,None,iterations=2)
    mask_red = cv2.inRange(hsv,red_lower,red_upper)
    mask_red = cv2.dilate(mask_red,None,iterations=2)

    #Finding contours of dots based on masks
    contours_green, _ = cv2.findContours(mask_green.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    contours_red, _ = cv2.findContours(mask_red.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    # Function to calculate centers of contours
    def calculate_centers(contours):
        centers = []
        for contour in contours:
            # Calculate the bounding rectangle of the contour
            x, y, w, h = cv2.boundingRect(contour)
            # Calculate the center of the bounding rectangle
            center_x = x + w // 2
            center_y = y + h // 2
            # Append the center coordinates to the list
            centers.append((center_x, center_y))
        return centers

    # Calculate centers of green dots
    green_dot_centers = calculate_centers(contours_green)

    # Calculate centers of red dots
    red_dot_centers = calculate_centers(contours_red)

    idx1 = 0
    # Print the centers of green dots
    print("Centers of Green Dots:")
    for idx, center in enumerate(green_dot_centers):
        print(f"Green Dot {idx + 1}: {center}")
        file3 = open("./Week13/CamRecLiner/ResCamRec/resgreen2.txt","a")
        print(str(idx),":",center[0],",",center[1],file=file3)
        file3.close()
        idx1 += idx

    idx2 = 0
    # Print the centers of red dots
    print("\nCenters of Red Dots:")
    for idx, center in enumerate(red_dot_centers):
        print(f"Red Dot {idx + 1}: {center}")
        file = open("./Week13/CamRecLiner/ResCamRec/resred2.txt","a")
        print(str(idx),":",center[0],",",center[1],file=file)
        file.close()
        idx2 += idx

    def extract_coordinates(input_file, index,colour):
        output_file = f'Week13/CamRecLiner/ResCamRec/{colour}/res{index}.txt'
        with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
            for line in infile:
                parts = line.strip().split(':')
                if len(parts) == 2:
                    idx, coordinates = parts
                    if idx.strip() == str(index):
                        outfile.write(coordinates.strip() + '\n')


    # Main function to process the input file
    def mainred(input_file):
        for i in range(idx2):
            extract_coordinates(input_file, i, "Red")
            
    def maingreen(input_file):
        for j in range(idx1):
            extract_coordinates(input_file,j,"Green")

    if __name__ == "__main__":
        input_file = './Week13/CamRecLiner/ResCamRec/resred2.txt'
        mainred(input_file)
        input_file1 = "./Week13/CamRecLiner/ResCamRec/resgreen2.txt'"
        maingreen(input_file1)

        
    # Optionally, visualize the centers on the image
    for center in green_dot_centers:
        cv2.circle(frame, center, 3, (0, 255, 0), -1)  # Draw a green circle at each green dot center

    for center in red_dot_centers:
        cv2.circle(frame, center, 3, (255, 255, 255), -1)  # Draw a red circle at each red dot center

    # Display the image with centers marked
    cv2.imshow('Image with Dot Centers', frame)

    name = "./Week13/CamRecLiner/Frames/frame" + str(index) + (".jpg")
    cv2.imwrite(name,frame)
    index+=1

    key = cv2.waitKey(1) & 0xFF
    
    if key == ord("p"):
        paused = not paused
        print("Paused" if paused else "Resumed")
    
    if key == ord("d"):
        break

#Destroy windows and release video and files
if not args.get("video",False):
    v.stop()
else:
    v.release()

cv2.destroyAllWindows()
