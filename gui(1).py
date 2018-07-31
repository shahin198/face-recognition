
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



#Set up GUI
window = Tk()  #Makes main window
window.wm_title("Face Recognition")
window.config(background="gray")
# ...........Menu func...........
def NewFile():
    print ("New File!")
    
def SaveFile():
    save_face_data()
    
def About():
    print ("This is a simple example of a menu")
#Menu....    
menu = Menu(window)
window.config(menu=menu)
filemenu = Menu(menu)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="New", command=NewFile)
filemenu.add_command(label="Save...", command=SaveFile)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=window.quit)

helpmenu = Menu(menu)
menu.add_cascade(label="Help", command=About)
# helpmenu.add_command(label="About...", command=About)
#.......Menu end.............


# In[3]:



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


# In[4]:


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


# In[5]:


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


# In[6]:



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


# In[7]:


#Slider window (slider controls stage position)
unknownFrame = Frame(window,highlightbackground="gray", highlightcolor="gray", highlightthickness=2, bg='gray',width=200, height=200)
unknownFrame.grid(row=0, column=0, padx=2, pady=2)


#Graphics window
liveFrame = Frame(window, width=640, height=480)
liveFrame.grid(row=0, column=1, padx=10, pady=5,sticky='ne')

profileFrame = Frame(window,  width=640, height=480)
profileFrame.grid(row=0, column=2, padx=10, pady=5,sticky='ne')


profileImgFrame=Frame(profileFrame,  width=640, height=100,highlightbackground="gray", highlightcolor="gray", bg='gray')
profileImgFrame.grid(row=1, column=0, padx=0, pady=0,sticky='ne')

profileInfoFrame=Frame(profileFrame,  width=640, height=200,highlightbackground="gray", highlightcolor="gray", bg='gray')
profileInfoFrame.grid(row=2, column=0,columnspan=2, padx=0, pady=0,sticky='ne')


togelFrame = Frame(window,  width=100, height=100)
togelFrame.grid(row=1, column=0, padx=10, pady=0,sticky='ne')


knownFrame = Frame(window,  width=640, height=100)
knownFrame.grid(row=1, column=1,columnspan=2, padx=10, pady=0,sticky='ne')


# In[8]:


flg=False
def togelFn(event):
    global flg    
   
    if flg==False:
        liveFrame.grid_forget()
        profileFrame.grid(row=0, column=1, padx=10, pady=5,sticky='ne')
        
        flg=True
    else:
        profileFrame.grid_forget()
        liveFrame.grid(row=0, column=1, padx=10, pady=5,sticky='news')
        
        flg=False
        
togel_btn = Label(togelFrame)
togel_btn.grid(row=0, column=0,padx=2, pady=2)
btn_Img=cv2.imread("live.jpg")    
cv2image1 = cv2.cvtColor(btn_Img, cv2.COLOR_BGR2RGBA)
cv2image1=cv2.resize(cv2image1, (100,100))
img1 = Image.fromarray(cv2image1)
imgtk = ImageTk.PhotoImage(image=img1)
togel_btn.imgtk = imgtk
togel_btn.configure(image=imgtk)
togel_btn.bind("<Button-1>",togelFn)


# In[9]:


infoFrame=Frame(profileInfoFrame,  width=640, height=200,highlightbackground="gray", highlightcolor="gray", bg='gray')
infoFrame.grid(row=0, column=0, padx=0, pady=0,sticky='ne')

editInfoFrame=Frame(profileInfoFrame,  width=640, height=200,highlightbackground="gray", highlightcolor="gray", bg='gray')
editInfoFrame.grid(row=0, column=0, padx=0, pady=0,sticky='ne')

Label(infoFrame, text="Id: ").grid(row=0,column=0, padx=2, pady=2,sticky='e')
lb_id=Label(infoFrame, text="0")
lb_id.grid(row=0,column=1, padx=2, pady=2,sticky='w')

def Edit():
    if int(person_id)>=0:
        print("call edit")
        editInfoFrame.grid(row=0, column=0, padx=0, pady=0,sticky='ne')

btn_edit = Button(infoFrame, text ="Edit", command = Edit, padx=2, pady=2)
btn_edit.grid(row=0, column=2,sticky='w')

Label(infoFrame, text="Name: ").grid(row=1,column=0, padx=2, pady=2,sticky='e')
lb_name=Label(infoFrame, text="Person Name")
lb_name.grid(row=1,column=1, padx=2, pady=2,sticky='w')


Label(infoFrame, text="First Time: ").grid(row=2,column=0, padx=2, pady=2,sticky='e')
lb_first_time=Label(infoFrame, text="12-7-2018")
lb_first_time.grid(row=2,column=1, padx=2, pady=2,sticky='w')

Label(infoFrame, text="Last Time: ").grid(row=3,column=0, padx=2, pady=2,sticky='e')
lb_last_time=Label(infoFrame, text="12-7-2018")
lb_last_time.grid(row=3,column=1, padx=2, pady=2,sticky='w')

Label(infoFrame, text="Address: ").grid(row=4,column=0, padx=2, pady=2,sticky='e')
lb_address=Label(infoFrame, text="Dhaka , Bangladesh")
lb_address.grid(row=4,column=1, padx=2, pady=2,sticky='w')

Label(infoFrame, text="About: ").grid(row=5,column=0, padx=2, pady=2,sticky='e')
lb_about=Label(infoFrame, text="..........")
lb_about.grid(row=5,column=1, padx=2, pady=2,sticky='w')


# lab1=Label(profileInfoFrame, text="label_1")
# lab1.grid(row=0,column=0, padx=2, pady=2)
# input_1 = Entry(profileInfoFrame)
# input_1.grid(row=0, column=1,columnspan=3, padx=2, pady=2)
# lab1=Label(profileInfoFrame, text="label_1")
# lab1.grid(row=1,column=0, padx=2, pady=2)
# input_1 = Entry(profileInfoFrame)
# input_1.grid(row=1, column=1,columnspan=3, padx=2, pady=2)
# l = Label(profileInfoFrame,text="123",bg="gray")
# l.place(x=25, y=25, anchor="center")


# In[10]:


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
    


# In[11]:



Label(editInfoFrame, text="Id: ").grid(row=0,column=0, padx=2, pady=2,sticky='e')
id_=Label(editInfoFrame, text="1")
id_.grid(row=0,column=1, padx=2, pady=2,sticky='w')

def View():
    print("call View")
    infoFrame.grid(row=0, column=0, padx=0, pady=0,sticky='ne')
    editInfoFrame.grid_forget()

btn_view = Button(editInfoFrame, text ="View", command = View, padx=2, pady=2)
btn_view.grid(row=0, column=2,sticky='w')

Label(editInfoFrame, text="Name: ").grid(row=1,column=0, padx=2, pady=2,sticky='e')

name=Entry(editInfoFrame)
name.grid(row=1,column=1, padx=2, pady=2,sticky='w')


Label(editInfoFrame, text="First Time: ").grid(row=2,column=0, padx=2, pady=2,sticky='e')
firstTime=Label(editInfoFrame, text="12-7-2018")
firstTime.grid(row=2,column=1, padx=2, pady=2,sticky='w')

Label(editInfoFrame, text="Last Time: ").grid(row=3,column=0, padx=2, pady=2,sticky='e')
lastTime=Label(editInfoFrame, text="12-7-2018")
lastTime.grid(row=3,column=1, padx=2, pady=2,sticky='w')

Label(editInfoFrame, text="Address: ").grid(row=4,column=0, padx=2, pady=2,sticky='e')

address=Entry(editInfoFrame)
address.grid(row=4,column=1, padx=2, pady=2,sticky='w')

Label(editInfoFrame, text="About: ").grid(row=5,column=0, padx=2, pady=2,sticky='e')

about=Entry(editInfoFrame)
about.grid(row=5,column=1, padx=2, pady=2,sticky='w')

def addNewPerson():
    
    print("Add new Person: ",person_id)
    personName=name.get()
    personInfo=(person_id,name.get(),address.get(),about.get(),firstTime['text'],lastTime['text'])
    res=insert_person_info(conection, personInfo)
    if res==True:
        print(personName)
        face_labelling(person_id,personName,True)
        path="testin/"+str(person_id)+".png"
        dis="testout/"+str(person_id)+".png"
        os.rename(path, dis)
        load_unknown()
        load_known()
        save_face_data()
    return
    
def updatePerson():
    print("Update Person: ")
    face_labelling(person_id,name.get(),True)
    personInfo=(name.get(),address.get(),about.get(),lastTime['text'],person_id_key)
    res=update_person_info(conection, personInfo)
    save_face_data()
    return

def Submit():
    
    if addFlg==True:
        addNewPerson()
    else:
        updatePerson()

btn_submit = Button(editInfoFrame, text ="Submit", command = Submit, padx=2, pady=2)
btn_submit.grid(row=6, column=2,sticky='w')

editInfoFrame.grid_forget()


# In[12]:



profileFrame.grid_forget()
#Capture video frames
lmain = Label(liveFrame)
lmain.grid(row=0, column=0)
# lmain1 = Label(liveFrame)
# lmain1.grid(row=0, column=1)


# In[13]:


addFlg=True
person_id=-1
def addProfile(event):
    
    global person_id
    selectFace = Label(profileImgFrame)
    selectFace.grid(row=0, column=0,padx=2, pady=2)

    if int(event.widget.my_name)>=0:
        unknown_face=cv2.imread("testin/"+unknown_faces[int(event.widget.my_name)])
        person_id=unknown_faces[int(event.widget.my_name)].split(".")[0]
        setPersonInfo(person_id,"+P_"+str(person_id),"","","","")
    else:
        unknown_face=cv2.imread("blank_face.jpg")
        person_id=int(event.widget.my_name)
        setPersonInfo(0,"","","","","")

    cv2image1 = cv2.cvtColor(unknown_face, cv2.COLOR_BGR2RGBA)
    cv2image1=cv2.resize(cv2image1, (100,100))
    img1 = Image.fromarray(cv2image1)
    imgtk = ImageTk.PhotoImage(image=img1)

    selectFace.imgtk = imgtk
    selectFace.configure(image=imgtk)
    addFlg=True
    
    infoFrame.grid(row=0, column=0, padx=0, pady=0,sticky='ne')
    editInfoFrame.grid_forget()
    


# Load Unknown IMage
def load_unknown():
    global unknown_faces
    unknown_faces=os.listdir("testin/")
    unkonwnTitel = Label(unknownFrame ,text="New Faces", width=10,justify=LEFT)        
    unkonwnTitel.grid(row=0, column=0, padx=2, pady=2)
    i=0
    indx=-1
    while i<5:
        if i<len(unknown_faces):
            unknown_face=cv2.imread("testin/"+unknown_faces[i])
            indx=i
        else:
            unknown_face=cv2.imread("blank_face.jpg")
            indx=-1

        cv2image1 = cv2.cvtColor(unknown_face, cv2.COLOR_BGR2RGBA)
        cv2image1=cv2.resize(cv2image1, (100,100))
        img1 = Image.fromarray(cv2image1)
        imgtk = ImageTk.PhotoImage(image=img1)
        #Capture video frames
        trainFrame = Label(unknownFrame)
        trainFrame.my_name=str(indx)
        trainFrame.grid(row=(i+1), column=0,columnspan=3, padx=2, pady=2)
        trainFrame.imgtk = imgtk
        trainFrame.configure(image=imgtk)
        trainFrame.bind("<Button-1>",addProfile)
        i=i+1
    
    


person_id_key=-1
def viewProfile(event):
    
    global person_id,person_id_key
    selectFace = Label(profileImgFrame)
    selectFace.grid(row=0, column=0,padx=2, pady=2)
    
    if int(event.widget.my_name)>=0:

        known_face=cv2.imread("testout/"+known_faces[int(event.widget.my_name)])
        person_id=known_faces[int(event.widget.my_name)].split(".")[0]
        person_info=select_personInfo_by_person_id(conection, person_id)
        if person_info!=None:
            person_id_key=person_info[0]
            
            setPersonInfo(person_info[1],person_info[2],person_info[3],person_info[4],person_info[5],person_info[6])
    else:
        known_face=cv2.imread("blank_face.jpg")
        person_id=int(event.widget.my_name)
        setPersonInfo(0,"","","","","")

    cv2image1 = cv2.cvtColor(known_face, cv2.COLOR_BGR2RGBA)
    cv2image1=cv2.resize(cv2image1, (100,100))
    img1 = Image.fromarray(cv2image1)
    imgtk = ImageTk.PhotoImage(image=img1)

    selectFace.imgtk = imgtk
    selectFace.configure(image=imgtk)
    addFlg=False
    
    infoFrame.grid(row=0, column=0, padx=0, pady=0,sticky='ne')
    editInfoFrame.grid_forget()
        
def load_known():
    global known_faces
    
    known_persons=select_persons_order_by_last_time(conection)
    print(known_persons)
    known_faces=os.listdir("testout/")
    i=0
    indx=-1
    while i<6:
        if i<len(known_faces):
            known_face=cv2.imread("testout/"+known_faces[i])
            indx=i
        else:
            known_face=cv2.imread("blank_face.jpg")
            indx=-1

        cv2image1 = cv2.cvtColor(known_face, cv2.COLOR_BGR2RGBA)
        cv2image1=cv2.resize(cv2image1, (100,100))
        img1 = Image.fromarray(cv2image1)
        imgtk = ImageTk.PhotoImage(image=img1)
        #Capture video frames
        knownImg = Label(knownFrame)
        knownImg.my_name=str(indx)
        knownImg.grid(row=0, column=i, padx=2, pady=2)
        knownImg.imgtk = imgtk
        knownImg.configure(image=imgtk)
        knownImg.bind("<Button-1>",viewProfile)
        name="name"
        name=name.replace(" ","\n")
        knownName = Label(knownFrame ,text=name, width=10,justify=LEFT)
        
        knownName.grid(row=1, column=i, padx=2, pady=2)
        
        i=i+1
        
load_unknown()
load_known()


# In[14]:


# new_face_names={}

unknown_face_encodings = []
unknown_face_links = []
unknown_face_counts = np.zeros(500,dtype=int)
unknown_face_times = np.zeros(500)
new_id=1


# In[15]:


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


# In[16]:


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
 


# In[17]:


def unknown_face_train(face_id):
    global unknown_face_encodings,unknown_face_links,totalParson,unknown_faces
    
    totalParson=totalParson+1
    person_id_=str(totalParson)
    
    path="collection_face/"+str(face_id)+"_"+str(2)+'.png'
    new_path="testin/"+person_id_+'.png'
    os.rename(path, new_path)
    
    unknown_faces.append(person_id_+'.png')
    
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
            
    load_unknown()


# In[18]:


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


# In[19]:


video_capture = cv2.VideoCapture(0)
# video_capture = cv2.VideoCapture('video/video.avi')
# video_capture = WebcamVideoStream(src=0).start()
# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
# new_face_encodings={}
# new_face_names={}


# In[20]:


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


# In[21]:


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


# In[22]:


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


# In[23]:


def findParent(unique_id):
    global new_person_names
    
    if new_person_names[""+unique_id][0]!=unique_id:
        new_person_names[""+unique_id][0]=findParent(new_person_names[""+unique_id][0])
        
    else:
        return unique_id
        

        


# In[24]:


# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi',fourcc, 25.0, (640,480))


# In[25]:



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
#                 seconds = end - start
#                 fps=1/seconds
            totalFram=totalFram+1
            totalSeconds=end-start
            fps=totalFram/totalSeconds
            cv2.putText(frame, "FPS:{:5.2f}".format(fps), (10, 25), font, 1, (0, 0, 255), 2)
            #Image view...
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            lmain.imgtk = imgtk
            lmain.configure(image=imgtk)
            # write the flipped frame
            out.write(frame)

#             lmain.after(10, faceRecg)
    


# In[26]:


# faceRecg()  
Process = threading.Thread(target=faceRecg)
Process.start()
window.mainloop()  #Starts GUI
window.destroy()
Process.join()
# Release handle to the webcam
# video_capture.stop()
video_capture.release()
cv2.destroyAllWindows()

