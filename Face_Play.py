
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



def yaml_loader(filepath):
 try:
     """Loads a yaml file"""
 #     data = enhancedyaml.load(open(filepath))
     with open(filepath,"r") as file_descriptor:
         data=load(file_descriptor)

     return data
 except:
     return {}
     pass
def yaml_dump(filepath,data):
 """Loads a yaml file"""
 with open(filepath,"w") as file_descriptor:
     data=dump(data,file_descriptor, default_flow_style=False)
     
 return data


# In[3]:


try:            

    new_face_encodings=yaml_loader("train_data/face_encodings.yaml")

    # face_encoding = new_face_encodings[face_id] 

    known_face_encodings=list(new_face_encodings.values())


    new_person_ids=yaml_loader("train_data/person_ids.yaml")

    # person_id = new_person_ids[face_id] 


    known_face_keys=list(new_person_ids.keys())
    known_face_values=np.array(list(new_person_ids.values()))
    print(known_face_values)
    
    link_face_ids=yaml_loader("train_data/link_face_ids.yaml")

    new_person_names=yaml_loader("train_data/person_names.yaml")

    # person_name = new_person_names[person_id]

    # known_person_names=list(new_person_names.values())
    # known_person_ids=list(new_person_names.keys())

    # print(known_face_keys)
    totalParson=len(new_person_names)
    
except:
    new_face_encodings={}
    known_face_encodings=[]
    new_person_ids={}
    known_face_keys=[] #face_id
    known_face_values==np.array() #person_id
    link_face_ids={}
    new_person_names={}
    totalParson=0
    pass 
print(totalParson)


# In[4]:


# new_face_encodings={}
# known_face_encodings=[]
# new_person_ids={}
# known_face_keys=[] #face_id
# known_face_values=[] #person_id
# new_person_names={}
# totalParson=0
def save_face_data():
    global new_face_encodings,new_person_ids,new_person_names
#     print(new_face_names)

    filePath="train_data/face_encodings.yaml" 
    yaml_dump(filePath,new_face_encodings)
    
    filePath="train_data/person_ids.yaml"
    yaml_dump(filePath,new_person_ids)
    
    
    filePath="train_data/link_face_ids.yaml"
    yaml_dump(filePath,link_face_ids)
    
    filePath="train_data/person_names.yaml"
    yaml_dump(filePath,new_person_names)
    
#     new_face_names={}
    print("Face Train Successfully")


# In[5]:



def create_connection(db_file):
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
        return conn
    except Error as e:
        print(e)
#     finally:
#         conn.close()
        
def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)   
        
def select_personInfo_by_person_id(conn, person_id):
    """
    Query tasks by priority
    :param conn: the Connection object
    :param priority:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM tblPersonInfo WHERE person_id=?", (person_id,))
    print(person_id)
    rows = cur.fetchall()
 
    for row in rows:
        print(row)
        return row
        
    return None

def select_persons_order_by_last_time(conn):
    """    
    :param conn: the Connection object
    :param priority:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM tblPersonInfo ORDER BY last_time ASC LIMIT 6")
    
    rows = cur.fetchall()
                
    return rows

def insert_person_info(conn, personInfo):
    """
    Create a new task
    :param conn:
    :param personInfo:
    :return:
    """
    
    sql = ''' INSERT INTO tblPersonInfo(person_id,name,address,about,first_time,last_time)
              VALUES(?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, personInfo)
    
    return True

def update_person_info(conn, personInfo):
    """
    
    :param conn:
    :param personInfo:
    :return:  id
    """
    sql = ''' UPDATE tblPersonInfo
              SET name = ? ,
                  address = ? ,
                  about = ? ,
                  last_time = ?
              WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, personInfo)
    
conection=None
def createDb():
    global conection
    database = "testdb.db"
    sql_create_personInfo_table = """ CREATE TABLE IF NOT EXISTS tblPersonInfo (
                                        id integer PRIMARY KEY,
                                        person_id integer NOT NULL UNIQUE,
                                        name text NOT NULL,
                                        address text,
                                        about text,
                                        first_time text,
                                        last_time text
                                    ); """
    
#  person_id, name, address, about, firstTime, lastTime
    # create a database connection
    conection = create_connection(database)
    if conection is not None:        
        # create person info table
        create_table(conection, sql_create_personInfo_table)
        
    else:
        print("Error! cannot create the database connection.")
        
createDb()


# In[6]:


def setPersonInfo(id_p,name_p,address_p,about_p,first_time_p,last_time_p):
#     View
    lb_id['text']=id_p
    lb_name['text']=name_p
    lb_first_time['text']=first_time_p
    lb_last_time['text']=last_time_p
    lb_address['text']=address_p
    lb_about['text']=about_p
    
#     Edit
    id_['text']=id_p
    name['text']=name_p
    firstTime['text']=first_time_p
    lastTime['text']=last_time_p
    address['text']=address_p
    about['text']=about_p
    


# In[7]:


# new_face_names={}

unknown_face_encodings = []
unknown_face_links = []
unknown_face_counts = np.zeros(500,dtype=int)
unknown_face_times = np.zeros(500)
new_id=1


# In[8]:


def clean_collection_folder():
    collection_list=os.listdir("collection_face/")
    i=0
    while i<len(collection_list):
        filename="collection_face/"+collection_list[i]
        try:
            os.remove(filename)
        except:
            pass
        i=i+1
        
clean_collection_folder()


# In[9]:


def unknown_face_delete(face_id):
    global unknown_face_encodings,unknown_face_links,unknown_face_counts
    i=0
    while i<len(unknown_face_links):
        if unknown_face_links[i]==face_id:
            del(unknown_face_links[i])
            del(unknown_face_encodings[i])
#             delete face file
            for i in range(unknown_face_counts[face_id]):
                filename="collection_face/"+str(face_id)+"_"+str(i+1)+'.png'
                try:
                    os.remove(filename)
                except:
                    pass
                
            unknown_face_counts[face_id]=0
        else:
            i=i+1  
 


# In[10]:


def unknown_face_train(face_id):
    global unknown_face_encodings,unknown_face_links,totalParson,unknown_faces
    
    totalParson=totalParson+1
    person_id_=str(totalParson)
    
    path="collection_face/"+str(face_id)+"_"+str(2)+'.png'
    new_path="testin/"+person_id_+'.png'
    os.rename(path, new_path)    
    
    
#             delete face file
    for i in range(unknown_face_counts[face_id]):
        filename="collection_face/"+str(face_id)+"_"+str(i+1)+'.png'
        try:
            os.remove(filename)
        except:
            pass    

#     unknown_face_links=[]
    i=0
    j=0
    
    while i<len(unknown_face_links):
        if unknown_face_links[i]==face_id:
            if j>0 and j<3:
                face_id=person_id_+"_"+str(time.time())
                auto_face_train(unknown_face_encodings[i],face_id,person_id_)
                person_name="+Person-"+str(person_id_)
                face_labelling(person_id_,person_name,False)
            j=j+1
            del(unknown_face_links[i])
            del(unknown_face_encodings[i])

        else:
            i=i+1    
            
    


# In[11]:


new_id=1
def unknown_face_collection(face_encoding,face_img):
    global unknown_face_encodings,unknown_face_links,unknown_face_counts,unknown_face_times,new_id
    
    height, width = face_img.shape[:2]
    if height<60:
        return 
    enc_len=len(unknown_face_encodings)
    value=1.0
    cr_time = time.time()
    if enc_len>0:
        index,value = compare_faces_final(unknown_face_encodings, face_encoding,0.4)
    if value <0.3:                  
        unknown_face_id = unknown_face_links[index]        
        time_df=cr_time-unknown_face_times[unknown_face_id]
        cnt=unknown_face_counts[unknown_face_id]+1
        if time_df>100:
            cnt=1
            unknown_face_delete(unknown_face_id)
        
        if cnt>3:
            unknown_face_train(unknown_face_id)
            unknown_face_counts[unknown_face_id]=0
        else:
            unknown_face_times[unknown_face_id]=cr_time
            unknown_face_encodings.append(face_encoding)
            unknown_face_links.append(unknown_face_id)
            unknown_face_counts[unknown_face_id]=cnt
            cv2.imwrite("collection_face/"+str(unknown_face_id)+"_"+str(cnt)+'.png',face_img)
        
    else:
        
        while unknown_face_counts[new_id]>0:
            time_df=cr_time-unknown_face_times[new_id]
            if time_df>100:
                unknown_face_delete(new_id)
                break
            else:
                new_id=new_id+1
                if new_id>=500:
                    new_id=1
                
        unknown_face_times[new_id]=cr_time        
        unknown_face_encodings.append(face_encoding)
        unknown_face_links.append(new_id)
        unknown_face_counts[new_id]=1
        cv2.imwrite("collection_face/"+str(new_id)+"_1.png",face_img)
        new_id=new_id+1
        if new_id>=500:
            new_id=1


# In[12]:


gst="nvcamerasrc ! video/x-raw(memory:NVMM), width=(int)640, height=(int)360,format=(string)I420, framerate=(fraction)30/1 ! nvvidconv flip-method=0 ! video/x-raw, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink"
video_capture = cv2.VideoCapture(gst)
# video_capture = cv2.VideoCapture(0)
# video_capture = cv2.VideoCapture('video/video.avi')
# video_capture = WebcamVideoStream(src=0).start()
# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
# new_face_encodings={}
# new_face_names={}


# In[13]:


def auto_face_train(face_encoding,face_id,person_id_):
    global new_face_encodings,known_face_encodings,known_face_values
    
    new_face_encodings[""+face_id]=face_encoding
    new_person_ids[""+face_id]=""+person_id_
    
    if person_id_ in link_face_ids.keys():
        link_face_ids[""+person_id_].append(face_id)
    else:
        link_face_ids[""+person_id_]=[face_id]
    
    known_face_encodings.append(face_encoding)
    known_face_keys.append([face_id])
#     known_face_values.append([person_id_])
    known_face_values=np.append(known_face_values,[person_id_])
#     print(known_face_values)


# In[14]:


def face_labelling(person_id_,person_name_,over_write):
    global new_person_names
#     print(person_id_,new_person_names[""+str(person_id_)],person_id_,person_name,over_write)
    if person_id_ in new_person_names.keys():
        person_name=new_person_names[""+person_id_][1]
        if person_name[0]=='+' or over_write==True:
            new_person_names[""+person_id_]=[person_id_,person_name_]
         
    else:
        new_person_names[""+person_id_]=[person_id_,person_name_]
        
#     print(person_id_,new_person_names[""+person_id_],person_id_,person_name,over_write)


# In[15]:


def combinePersonName(unique_ids,counts,best_id):
    global new_person_names,known_face_keys,known_face_values,new_person_ids,link_face_ids
    print("ids:[",unique_ids,"], cnts:[",counts,"]")
#     print("cnt:",counts)
    indexs = np.where(np.array(counts) >= 1)[0]
    if len(indexs)>1:
        person_ids =unique_ids[indexs]
        print("marge: ",person_ids)
        index = np.where(person_ids==best_id)[0]
        
        if index>=0:       
            unique_id=person_ids[0]
            if new_person_names[""+unique_id][1][0]=='+':
                for i in range(len(person_ids)):
                    if new_person_names[""+person_ids[i]][1][0]!='+':
                        unique_id=person_ids[i]

            
            for i in range(len(person_ids)):
                tmp_id=person_ids[i]
                print(tmp_id,unique_id)
                if tmp_id != unique_id:
                    link_face_ids[""+unique_id]=link_face_ids[""+unique_id]+link_face_ids[""+tmp_id]
                    for face_id in link_face_ids[""+tmp_id]:
                        new_person_ids[""+face_id]=""+unique_id                    
                    
                    known_face_values[known_face_values ==tmp_id] =unique_id
                    # remove face image...    
                    filename="testin/"+tmp_id+'.png'
                    try:
                        os.remove(filename)
                    except:
                        pass
                    
            
            load_unknown()
            return True,unique_id
        
    return False,""


# In[16]:


def findParent(unique_id):
    global new_person_names
    
    if new_person_names[""+unique_id][0]!=unique_id:
        new_person_names[""+unique_id][0]=findParent(new_person_names[""+unique_id][0])
        
    else:
        return unique_id
        

        


# In[17]:


# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi',fourcc, 25.0, (640,480))


# In[18]:



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
    while True:
        start1 = time.time()
         
        # Grab a single frame of video
        ret,frame = video_capture.read()
        
#         print(frame)
        if ret==True:
#             cv2.imwrite("mainImg.png",frame)
            

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = frame[:, :, ::-1]

            # Only process every other frame of video to save time
            if process_this_frame:
                # Find all the faces and face encodings in the current frame of video
                face_locations = face_locations_fn(rgb_small_frame,1,"cnn")

#                     print(face_locations)
                face_encodings = face_encodings_fn(rgb_small_frame, face_locations)


                face_names = []
                i=0
                for face_encoding in face_encodings:
#                         print(len(face_encoding),face_encoding)
                    face=face_locations[i]
                    img=frame[face[0]:face[2],face[3]:face[1]]
                    name = "Unknown"
#                         known_face_values=np.array(list(new_person_ids.values()))

                    # See if the face is a match for the known face(s)
        #             matches,values = compare_faces(known_face_encodings, face_encoding,0.4)
                    if len(known_face_encodings)>0:                            
                        indexs,index,value = compare_faces(known_face_encodings, face_encoding,0.4)

            #             print(face_locations[i])
                        # top matching face.
                        if value <=0.4:
#                                 print(value)
                            person_ids = known_face_values[indexs]
                            unique_ids,counts=np.unique(person_ids,return_counts=True)
#                                 print(index,new_person_names)
                            person_id_=known_face_values[index]
#                                 print(index,person_id_)
#                                 name,person_id_=combinePersonName(unique_ids,counts)
                            name=new_person_names[""+person_id_][1]                            
                            height, width = img.shape[:2]
                            if value<=0.3 and height>=60:
                                if len(unique_ids)>1:
                                    print(person_id_)
                                    flg,pId=combinePersonName(unique_ids,counts,person_id_)
                                    if flg==True:
                                        person_id_=pId
                                if value>=0.1:
                                    face_id=person_id_+"_"+str(time.time())

                                    auto_face_train(face_encoding,face_id,person_id_)
                        else:
                            unknown_face_collection(face_encoding,img)

                    else:
                        unknown_face_collection(face_encoding,img)

                    i=i+1
                    face_names.append(name)

            process_this_frame = not process_this_frame

            i=0
            # Display the results
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                
                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), colors[i], 1)
                i=i+1
                i=i%10

                # Draw a label with a name below the face
#                     cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)

                cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.8, (255, 255, 255), 1)

            # Display the resulting image
        #     cv2.imshow('Video', frame)

             # End time
            end = time.time()
            # Time elapsed
            seconds = end - start1
            fet=1/seconds
            totalFram=totalFram+1
            totalSeconds=end-start
            fps=totalFram/totalSeconds
            cv2.putText(frame, "FPS:{:5.2f}".format(fps), (10, 25), font, 1, (0, 0, 255), 2)
            cv2.putText(frame, "FET:{:5.2f}".format(fet), (10, 55), font, 1, (0, 0, 255), 2)
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
            # write the flipped frame
#             out.write(frame)

#             lmain.after(10, faceRecg)
    


# In[19]:


faceRecg()  

# Release handle to the webcam
# video_capture.stop()
video_capture.release()
cv2.destroyAllWindows()

