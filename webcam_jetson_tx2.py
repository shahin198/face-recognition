import numpy as np
import cv2
import time

gst="nvcamerasrc ! video/x-raw(memory:NVMM), width=(int)640, height=(int)480,format=(string)I420, framerate=(fraction)30/1 ! nvvidconv flip-method=0 ! video/x-raw, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink"
cap = cv2.VideoCapture(gst)
totalFram=0
start = time.time()
while (True):
    ret, frame = cap.read()
    end = time.time()
    totalFram=totalFram+1
    totalSeconds=end-start
    fps=totalFram/totalSeconds
    font = cv2.FONT_HERSHEY_DUPLEX
    cv2.putText(frame, "FPS:{:5.2f}".format(fps), (10, 25), font, 1, (0, 0, 255), 2)
   
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
