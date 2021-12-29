from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

dir_local = "/home/pi/ECE496_CAPSTONE/Photos"
dir_drive = "14Vbz-_6q6RFBF7vTK1RzSnQMVQ9dn9N7"

gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

filenames_local = os.listdir(dir_local)

for filename_local in filenames_local:
    file_drive = drive.CreateFile({'parents': [{'id': dir_drive}]})
    file_drive['title'] = filename_local
    file_drive.SetContentFile(os.path.join(dir_local, filename_local))
    file_drive.Upload()