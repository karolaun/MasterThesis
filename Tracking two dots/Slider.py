#Disclaimer:
#Code taken from here: https://www.geeksforgeeks.org/detecting-objects-of-similar-color-in-python-using-opencv/?ref=lbp

#Implementing a slider to tweek all values for upper and lower boundaries for red and green.

import cv2 as cv	


cv.namedWindow('Tracking')
def nothing(x):
    pass
 
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
 
 #Making a mask
    l_h = cv.getTrackbarPos("LH",
                             "Tracking")
    # find LS trackbar position
    l_s = cv.getTrackbarPos("LS",
                             "Tracking")
    # find LV trackbar position
    l_v = cv.getTrackbarPos("LV", 
                             "Tracking")
    # find HH trackbar position
    h_h = cv.getTrackbarPos("HH", 
                             "Tracking")
    # find HS trackbar position
    h_s = cv.getTrackbarPos("HS",
                             "Tracking")
    # find HV trackbar position
    h_v = cv.getTrackbarPos("HV",
                             "Tracking")
    # create a given numpy array
    l_b = np.array([l_h, l_s,
                    l_v])
    # create a given numpy array
    u_b = np.array([h_h, h_s,
                    h_v])
    mask1 = cv.inRange(hsv,l_b,u_b) #Changed for red as well to tune the colour.
    mask1 = cv.erode(mask1,None,iterations=2)
    mask1 = cv.dilate(mask1,None,iterations=2)