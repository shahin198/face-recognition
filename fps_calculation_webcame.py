
# coding: utf-8

# In[1]:


import numpy as np
import cv2
import time, threading

# print(cv2.getBuildInformation())
vs = cv2.VideoCapture(0)
totalFram=0
start = time.time()
while (True):
    ret,frame = vs.read()
#     print(frame.shape)
    if ret==True:
        
        # End time
        end = time.time()
        # Time elapsed
    #                 seconds = end - start
    #                 fps=1/seconds
        totalFram=totalFram+1
        totalSeconds=end-start
        fps=totalFram/totalSeconds
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, "FPS:{:5.2f}".format(fps), (10, 25), font, 1, (0, 0, 255), 2)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

vs.release()
cv2.destroyAllWindows()

