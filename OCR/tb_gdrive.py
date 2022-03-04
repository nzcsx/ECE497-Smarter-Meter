import OCR.gdrive_load as load
import os

drive = load.connect()

img_dir = "1yyvOtfKZ-9LHFsmysg8ONTKvd0MnBAqV"
DATA_SAVE_PATH = "/Users/dongxuening/Desktop/capstone_code/OCR/contents"
# if not os.path.isdir(DATA_SAVE_PATH):
#     print("Path ", DATA_SAVE_PATH, "has not formed")
#     os.mkdir(DATA_SAVE_PATH)
#load.download_images(drive, dir_id=img_dir)
load.download_images_by_id(drive, '1EZrd7TrhysRePK5DvNdIjMJShEmy6nqp', DATA_SAVE_PATH, "img_test")