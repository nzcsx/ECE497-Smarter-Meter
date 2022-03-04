import torch
import torch.nn as nn
import torch.nn.functional as F
from datetime import datetime
import OCR.gdrive_load as load

import matplotlib.pyplot as plt  # for plotting
import torch.optim as optim  # for gradient descent

torch.manual_seed(1)  # set the random seed

# import all libraries to be used
import numpy as np
import time
import matplotlib.pyplot as plt

import torch.optim as optim
import torchvision
from torch.utils.data.sampler import SubsetRandomSampler
import torchvision.transforms as transforms

from torchvision import datasets, models, transforms
from torch.utils.data import TensorDataset
import random
from PIL import Image
import glob

import os
import torchvision.models
import cv2

import OCR.extraction as extract
import OCR.screen_split as split
import shutil

#Artifical Neural Network Architecture
class ANNClassifier(nn.Module):
    def __init__(self):
        super(ANNClassifier, self).__init__()
        self.fc1 = nn.Linear(256 * 4 * 7, 32)
        self.fc2 = nn.Linear(32, 10)

    def forward(self, x):
        x = x.view(-1, 256 * 4 * 7) #flatten feature data
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x


def OCR(img_path):
    print("Original Image: ")
    device = torch.device('cpu')
    img = Image.open(img_path)
    # img = img.rotate(270)
    plt.imshow(img)
    #plt.show()
    labels = ['10', '10', '10', '10', '10', '10']  # label 10 refers to unknown label

    if os.path.exists('Datasets_frames/'):
        shutil.rmtree('Datasets_frames/')
        os.makedirs('Datasets_frames/')
    else:
        os.makedirs('Datasets_frames/')

    DATA_SAVE_PATH = "Datasets_digits/"
    if not os.path.isdir(DATA_SAVE_PATH):
        print("Path ", DATA_SAVE_PATH, "has not formed")
        os.mkdir(DATA_SAVE_PATH)

    for i in range(11):
        if not os.path.isdir(DATA_SAVE_PATH + str(i) + '/'):
            print("Path ", DATA_SAVE_PATH + str(i) + '/', "has not formed")
            os.mkdir(DATA_SAVE_PATH + str(i) + '/')

    fail = [0, 0, 0]
    print("Screen Extract:")
    save_name = None
    # Extract the screen
    for file in glob.glob(img_path):
        try:
            f = extract.frameExtractor(image=None,
                               src_file_name=file,
                               dst_file_name='Datasets_frames/' + str(file).split('/')[-1],
                               return_image=False,
                               output_shape=(400, 100))
            print("saved_name", 'Datasets_frames/' + str(file).split('/')[-1])
            save_name = 'Datasets_frames/' + str(file).split('/')[-1]
            f.extractAndSaveFrame()
        except:
            fail[0] += 1

    print("Screen reading splitted into digits:")
    df = cv2.imread(img_path)
    for i in range(1):
        file_name = 'digits_'
        src_file_name = "Datasets_frames/%s" % file_name
        # print("saved", src_file_name)

        try:
            cutter = split.cutDigits(src_file_name=save_name, labels=labels)

            images_x = cutter.get_bounding_box_dummy()
            cutter.save_to_folder()
            paths = cutter.get_paths()

            for img in images_x:
                cv2.imshow(img)

        except:
            fail[1] += 1

    model_path = "model_2.pth"
    transform = transforms.Compose([transforms.Resize((180, 256)),
                                    transforms.ToTensor()])

    print("Digit Recognition:")
    img = Image.open(save_name)
    plt.imshow(img)
    #plt.show()

    alexNet = torchvision.models.alexnet(pretrained=True)
    ALNC = alexNet.features

    model = ANNClassifier()
    device = torch.device('cpu')
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.eval()

    labels = []
    reading = 0

    for p in paths:
        img = Image.open(p)

        img = transform(img)
        img = torch.unsqueeze(img, 0)

        output_p = model(ALNC(img))

        # select index with maximum prediction score
        pred_p = output_p.max(1, keepdim=True)[1]
        labels.append(pred_p[0].item())
        reading = reading * 10 + int(pred_p[0].item())

    print("label =", labels)
    print("reading =", reading)

    return reading

def get_readings(filenames):
    readings = []
    for file in filenames:
        readings.append(OCR(file))
    return readings

def record_power(dir_id):
    drive = load.connect()
    DATA_SAVE_PATH = "/Users/dongxuening/Desktop/capstone_code/OCR/contents"
    filename, img_path = load.download_images(drive=drive, dir_id=dir_id, save_path=DATA_SAVE_PATH)

    time, readings = [], []
    for file in filename:
        name = str(filename).split(".")
        curr = datetime.strptime(name[0], "%Y_%m_%d-%H_%M_%S")
        time.append(curr.strftime('%b-%d-%Y %H:%M:%S'))

    readings = get_readings(img_path)

    # remove all files and folders
    # if not os.path.isdir("/Datasets_digits"):
    #     os.rmdir("Datasets_digits")
    #     print("removed:", "Datasets_digits")
    #
    # if not os.path.isdir("/Datasets_frames"):
    #     os.rmdir("Datasets_frames")
    #     print("removed:", "Datasets_frames")
    #
    # if not os.path.isdir("/contents"):
    #     os.rmdir("/contents")
    #     print("removed:", "contents")
    return time, readings
