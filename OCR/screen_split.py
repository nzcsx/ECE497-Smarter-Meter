import cv2
import os
import pandas as pd
import shutil


class cutDigits:

    def __init__(self, image=None, src_file_name=None, dst_folder_name='Datasets_digits', last_digit=6, labels=None):
        """
        The aim of this class is to extract digits from the frame-only preprocessed image.
        We to delimit digits by bounding boxes.
        We tried several approaches, but we present here the most successful one, a "dummy" yet efficient approach.
        :param image: RGB image (numpy array NxMx3) of a SLICED SCREEN. If image is None, the image will be extracted from src_filename
        :param src_file_name: filename of a SLICED SCREEN to load the source image (e.g. HQ_digital_preprocessing/0a07d2cff5beb0580bca191427e8cd6e1a0eb678.jpg)
        :param dst_folder_name: home FOLDERname where to save the extracted digits.
        :param last_digit: int, the number of digits you want to extract starting from the left (0 = no digits / 4 = all four digits).
        :param labels: list, list of labels corresponding to the image, e.g. if th image shows 123.45, the labels will be ['x',1,2,3].
        """
        if image is None:
            self.image = cv2.imread(src_file_name)
        else:
            self.image = image

        self.src_file_name = src_file_name
        self.dst_folder_name = dst_folder_name
        self.last_digit = last_digit
        self.labels = labels

        self.box_size = None
        self.boxes = []
        self.paths = []

    def get_bounding_box_dummy(self):
        """
        Use this method to get bounding boxes and extract numbers by dividing the area in 4 equal parts ("dummy" yet efficient approach).
        """

        self.boxes = []
        self.box_size = 263 / 6  # self.image.shape[1]/6
        # self.image = self.image[10:280, 18:42]

        modified = False

        for i in range(self.last_digit):
            inf = i * self.box_size + 9
            sup = (i + 1) * self.box_size + 9
            self.boxes += [self.image[16:42, int(inf):int(sup)]]
            # inf = i * self.box_size
            # sup = (i+1) * self.box_size
            # self.boxes += [self.image[:, int(inf):int(sup)]]

        return self.boxes

    def save_to_folder(self):
        """
        Use this method to save the extracted bounding boxes.
        """
        if self.dst_folder_name is None:
            return

        for i in range(len(self.boxes)):
            if self.labels:
                box = self.boxes[i]
                label = self.labels[i]
                src_file_name = self.src_file_name.split('/')[-1].split('.')[0]
                dst_file_name = 'Datasets_digits/%s/%s_%s.jpg' % (label, src_file_name, str(i))
                self.paths.append(dst_file_name)
                cv2.imwrite(dst_file_name, box)

            else:
                pass

            # else :
        #      box = self.boxes[i]
        #     src_file_name = self.src_file_name.split('/')[-1].split('.')[0]
        #    dst_file_name = 'Datasets_digits/%s/%s_%s.jpg' % ('missing_label', src_file_name, str(i))
        #    cv2.imwrite(dst_file_name, box)

    def get_paths(self):
        return self.paths

# --------------------- End of the class -----------------------------------