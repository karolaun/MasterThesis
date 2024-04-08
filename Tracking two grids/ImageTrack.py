import cv2
import numpy as np
import matplotlib.pyplot as plt
 
# Load the image
image = cv2.imread('grids/Grids.png')
 
# Convert image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
plt.imshow(gray)
 
# Harris corner detection
corners = cv2.cornerHarris(gray, 2, 3, 0.04)
 
# Threshold corners to get strong corners
threshold = 0.01 * corners.max()
 
# Mark corners belonging to the first grid (e.g., red) in red
image_with_corners = image.copy()
image_with_corners[corners > threshold] = [0, 0, 255]
 
plt.imshow(image_with_corners)
 
# Mark corners belonging to the second grid (e.g., green) in green
# Assuming the second grid is green, you may need to adjust the color range
green_lower = np.array([35, 50, 50], dtype=np.uint8)
green_upper = np.array([85, 255, 255], dtype=np.uint8)
red_lower = np.array([0, 100, 100], np.uint8)
red_upper = np.array([10, 255, 255], np.uint8)
 
#Check of boundaries
blank = np.zeros_like(image)
blank[:] = green_lower
plt.imshow(blank)
plt.show()
 
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
mask_green = cv2.inRange(hsv, green_lower, green_upper)
mask_green = cv2.dilate(mask_green,None,iterations=2)
mask_red = cv2.inRange(hsv,red_lower,red_upper)
mask_red = cv2.dilate(mask_red,None,iterations=2)
 
plt.imshow(mask_red)
plt.show()
plt.imshow(mask_green)
plt.show()
 
contours1, _ = cv2.findContours(mask_green, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours2, _ = cv2.findContours(mask_red,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
 
for contour in contours1:
    x = [point[0][0] for point in contour]  # Extract x coordinates from each point in the contour
    y = [point[0][1] for point in contour]  # Extract y coordinates from each point in the contour
    plt.plot(x, y,"o", color='green',markersize=0.5)  # Plot the contour
 
# Plot contours from contours2
for contour in contours2:
    x = [point[0][0] for point in contour]  # Extract x coordinates from each point in the contour
    y = [point[0][1] for point in contour]  # Extract y coordinates from each point in the contour
    plt.plot(x, y,"o", color='red',markersize=0.5)  # Plot the contour
 
# Set plot labels and title
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Contours Plot')
 
# Show the plot
plt.grid(True)
plt.gca().invert_yaxis()  # Invert y-axis to match the image coordinates
plt.show()