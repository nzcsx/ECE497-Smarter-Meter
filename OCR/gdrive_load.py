from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
import os
def connect():
    gauth = GoogleAuth()
    # Create local webserver and auto handles authentication.
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)  # Create GoogleDrive instance with authenticated GoogleAuth instance
    return drive

def download_images(drive, dir_id, save_path, delete = True):
    if not os.path.isdir(save_path):
        print("Path ", save_path, "has not formed")
        os.mkdir(save_path)

    request = "'" + dir_id + "' in parents and trashed=false"
    # Auto-iterate through all files in the root folder.
    file_list = drive.ListFile({'q': request}).GetList()
    file_ids, filenames = [], []
    for file1 in file_list:
        print('title: %s, id: %s' % (file1['title'], file1['id']))
        filename = str(file1['title']).split(".")
        if filename[-1] == 'jpg':
            file_ids.append(file1['id'])
            filenames.append(file1['title'])

    img_paths = []
    for idx, file_id in enumerate(file_ids):
        file = drive.CreateFile({'id': file_id})
        img_path = save_path + "/img_"+str(idx)+".jpg"
        img_paths.append(img_path)
        file.GetContentFile(img_path)  # Download file as 'catlove.png'.

    if delete:
        delete_images(drive, dir_id)

    return filenames, img_paths

def delete_images(drive, dir_id):
    request = "'" + dir_id + "' in parents and trashed=false"
    # Auto-iterate through all files in the root folder.
    file_list = drive.ListFile({'q': request}).GetList()
    for file1 in file_list:
        file1.Trash()

def download_images_by_id(drive, file_id, save_path, filename):
    if not os.path.isdir(save_path):
        print("Path ", save_path, "has not formed")
        os.mkdir(save_path)

    file = drive.CreateFile({'id': file_id})
    file.GetContentFile(save_path+ "/" + filename+'.jpg') # Download file as 'catlove.png'.
    return save_path+ "/" + filename+'.jpg'