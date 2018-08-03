
# coding: utf-8

# In[1]:


# sudo apt-get install cmake
# pip3 install face_recognition
from face_recognition import load_image_file,compare_faces_final,compare_faces,face_locations_fn,face_encodings_fn
# pip3 install opencv-contrib-python
import cv2
# pip3 install imutils
import imutils
# pip3 search yaml
# pip3 install pyyaml
from yaml import load, dump
# import enhancedyaml
import os
import requests
# sudo apt-get install python3-tk
from tkinter import *
import time, threading
from PIL import ImageTk, Image
import numpy as np

 
import sqlite3
from sqlite3 import Error

from imutils.video import WebcamVideoStream


# In[2]:


# new_face_names={}

unknown_face_encodings = []
unknown_face_links = []
unknown_face_counts = np.zeros(500,dtype=int)
unknown_face_times = np.zeros(500)
new_id=1


# In[3]:



# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
# new_face_encodings={}
# new_face_names={}


# In[4]:


gst="nvcamerasrc ! video/x-raw(memory:NVMM), width=(int)640, height=(int)360,format=(string)I420, framerate=(fraction)30/1 ! nvvidconv flip-method=0 ! video/x-raw, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink"
# video_capture = cv2.VideoCapture(gst)
# video_capture = cv2.VideoCapture(0)
video_capture = cv2.VideoCapture(1) 
# video_capture.set(3,576) # CV_CAP_PROP_FRAME_WIDTH Width of the frames in the video stream.
# video_capture.set(4,432) # CV_CAP_PROP_FRAME_HEIGHT Height of the frames in the video stream.

# video_capture = WebcamVideoStream(src=0).start()
# Get a reference to webcam #0 (the default one)
# new_face_encodings={}
# known_face_encodings=[]
# known_face_keys=[] #face_id
# known_face_values=[] #person_id_
# new_person_names={}
# totalParson=0
totalFram=0
colors=[(0,0,255),( 223, 71, 38 ),( 234, 199, 37 ),( 234, 234, 37 ),( 28, 213, 48),( 28, 213, 190 ),( 28, 165, 213 ),( 28, 90, 213 ),( 126, 28, 213 ),( 196, 28, 213 ),( 213, 28, 115 )]
def faceRecg():
    global process_this_frame,face_locations,face_encodings,face_names,totalParson,known_face_values,totalFram
    start = time.time()
    font = cv2.FONT_HERSHEY_DUPLEX
    seconds=0
    while True:
        
         
        # Grab a single frame of video
        ret,frame = video_capture.read()
        
        start1 = time.time()
        x=2
        rz=1/x
#         print(frame)
        if ret==True:
            small_frame = cv2.resize(frame, (0, 0), fx=rz, fy=rz)
#            

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]

            # Only process every other frame of video to save time
            if process_this_frame:
                # Find all the faces and face encodings in the current frame of video
                face_locations = face_locations_fn(rgb_small_frame,1,"cnn")

            i=0
            # Display the results
            for (top, right, bottom, left) in face_locations:
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                left*=x
                top*=x
                right*=x
                bottom*=x
                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), colors[i], 1)
                i=i+1
                i=i%10

             # End time
            end = time.time()
            # Time elapsed
#            4  seconds = seconds+end - start1
            
            
            totalFram=totalFram+1
            totalSeconds=end-start
#             fet=totalFram/seconds
            fps=totalFram/totalSeconds
#             print(end - start1,i)
            cv2.putText(frame, "FPS:{:5.2f}".format(fps), (10, 25), font, 1, (0, 0, 255), 2)
#             cv2.putText(frame, "FET:{:5.2f}".format(fet), (10, 55), font, 1, (0, 0, 255), 2)
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
            # write the flipped frame
            out.write(frame)

#             lmain.after(10, faceRecg)
    


# In[ ]:


faceRecg()  

# Release handle to the webcam
# video_capture.stop()
video_capture.release()
cv2.destroyAllWindows()

