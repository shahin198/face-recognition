# If use Gpu first install cuda properly

https://github.com/shahin198/cuda-programming/blob/master/README.md

![alt text](https://github.com/shahin198/face-recognition/blob/master/Screenshot%20from%202018-08-01%2009-50-50.png)
# face-recognition
```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get dist-upgrade

sudo apt-get install python3
sudo apt-get -y install python3-pip
sudo apt-get install cmake
pip3 install face_recognition
python3 -m pip install jupyter
pip3 install opencv-contrib-python

pip3 install imutils
pip3 install opencv-python 

pip3 search yaml
pip3 install pyyaml
pip3 install Pillow
python3 -m pip install Pillow

python3 -m pip install jupyter
sudo pip3 install dlib
sudo apt-get install python3-tk

pip3 install tensorflow-gpu
pip3 install tflearn
pip3 install tqdm
pip3 install --user matplotlib

sudo apt-get install python3-flask
```
# check dlib is cuda support
```
>>> import dlib
>>> print(dlib.DLIB_USE_CUDA)
True
>>> exit()

```
# opencv
https://www.jetsonhacks.com/2018/05/28/build-opencv-3-4-with-cuda-on-nvidia-jetson-tx2/

```
print(cv2.getBuildInformation())
```
# Sqlite Browser
```
Update the cache using:

   sudo apt-get update

Install the package using:

   sudo apt-get install sqlitebrowser
   
```
