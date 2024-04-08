from picamera import PiCamera
from time import sleep
 
camera = PiCamera()
 
Camera.strart_preview()
 
#Test for video, later removed for images. It was tried because the location was unclear.
try:
    camera.start_recording("/home/karolineaune/Desktop/video.h264")
    sleep(5)
    camera.stop_recording()
    camera.stop_preview()
except:
    sleep(5)
    print("It did not work")
    camera.stop_preview()
 
camera.capture("./focusingX.jpg") #Switched X for which iteration it was. First iterations are not captured with camera.