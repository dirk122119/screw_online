# MIT License
# Copyright (c) 2019 JetsonHacks
# See license
# Using a CSI camera (such as the Raspberry Pi Version 2) connected to a
# NVIDIA Jetson Nano Developer Kit using OpenCV
# Drivers for the camera and OpenCV are included in the base image

import cv2
import numpy as np
import os
os.path.abspath(os.getcwd())
# gstreamer_pipeline returns a GStreamer pipeline for capturing from the CSI camera
# Defaults to 1280x720 @ 60fps
# Flip the image by setting the flip_method (most common values: 0 and 2)
# display_width and display_height determine the size of the window on the screen


def gstreamer_pipeline(
    sensor_id=0,
    capture_width=1280,
    capture_height=720,
    display_width=1280,
    display_height=720,
    framerate=30,
    flip_method=0,
):
    return (
        "nvarguscamerasrc sensor-id=%d sensor-mode=3 ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, "
        "format=(string)NV12, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            sensor_id,
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )


def show_camera():
    # To flip the image, modify the flip_method parameter (0 and 2 are the most common)
    print(gstreamer_pipeline(flip_method=0))
    cap1 = cv2.VideoCapture(gstreamer_pipeline(sensor_id=0,flip_method=0))
    cap2 = cv2.VideoCapture(gstreamer_pipeline(sensor_id=1,flip_method=0))
    num=1
    while(True):
        ret_val, img1 = cap1.read()
        ret_val, img2 = cap2.read()
        fram3=np.hstack((img1,img2))
        ##cv2.imshow("CSI Camera1", img1)
        ##cv2.imshow("CSI Camera2", img2)
        cv2.imshow('combocam',fram3)
        cv2.moveWindow('combocam2',0,500)
        if cv2.waitKey(1) & 0xFF == ord('s'):
            cv2.imwrite(os.path.abspath(os.getcwd())+"/images/%d.png"%(num), img1, [cv2.IMWRITE_PNG_COMPRESSION, 9])
            break
        '''
        if cv2.waitKey(1)& 0xFF == ord('c'):
            cv2.imwrite(os.path.abspath(os.getcwd())+"/images/%d.png"%(num), img1, [cv2.IMWRITE_PNG_COMPRESSION, 9])
            
            print(num)
            print("capture----->"+os.path.abspath(os.getcwd())+"/images/%d.png"%(num))
            num=num+1
        '''    
    cap1.release()
    cap2.release()
    cv2.destroyAllWindows()
    return img1
        


if __name__ == "__main__":
    show_camera()
