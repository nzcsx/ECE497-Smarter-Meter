import sys
sys.path.append('/home/pi/ECE496_CAPSTONE')

import os, time, pydrive
import RPi.GPIO as GPIO
from time import sleep
from picamera import PiCamera
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# File counting reference:
# https://stackoverflow.com/questions/2632205/how-to-count-the-number-of-files-in-a-directory-using-python 
max_num_pics = 10
time_interval = 1
dir_local = '/home/pi/ECE496_CAPSTONE/Photos'
dir_drive = '14Vbz-_6q6RFBF7vTK1RzSnQMVQ9dn9N7'

camera = PiCamera()
gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)

# count #files
    #path, dirs, files = next(os.walk(dir_local))
    #pics_count = len(files)

# keep taking phots and upload to drive
flag = True
while flag:
    # take max_num_pics amount of photos
    for i in range(max_num_pics):
        sleep(time_interval)
        filename_local = time.strftime('%Y_%m_%d-%H_%M_%S') + '.jpg'
        GPIO.output(18,GPIO.HIGH)
        camera.capture(os.path.join(dir_local, filename_local))
        GPIO.output(18,GPIO.LOW)
        
    # upload these photo to google drive
    filenames_local = os.listdir(dir_local)
    for filename_local in filenames_local:
        file_drive = drive.CreateFile({'parents': [{'id': dir_drive}]})
        file_drive['title'] = filename_local
        file_drive.SetContentFile(os.path.join(dir_local, filename_local))
        file_drive.Upload()
    
    flag = False