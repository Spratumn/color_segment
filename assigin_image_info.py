#!/usr/bin/python
#coding:utf-8 

import cv2
import os
import numpy as np
import sys
import ast
from PySide2.QtWidgets import QMainWindow, QFileDialog, QApplication
from PySide2.QtGui import QImage, QPixmap
from PySide2.QtCore import Qt

from ui.ui_color_segment import Ui_MainWindow


class MyPS(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.label.setAlignment(Qt.AlignCenter)

        self.center = [471, 335]
        self.left_top = [471, 335]
        self.bottom_right = [472, 336]
        self.mat = np.zeros([1, 1, 3], np.uint8)
        self.resize_rate = 1.0
        self.points = []
        self.point_nums = 2

        self.root_dir = ''
        self.file_names = []
        self.file_index = 0
        self.image_info = {}
        self.image_suffix = '.png'
        self.image_info_result_name = 'image_info'

        
        self.actionOpen.triggered.connect(self.load_file)
        self.pushButtonNext.clicked.connect(self.next_image)
        self.pushButtonLast.clicked.connect(self.last_image)
        
    def load_file(self):
        self.root_dir = QFileDialog.getExistingDirectory(self, './')
        image_names = os.listdir(self.root_dir)
        for file_name in image_names:
            if file_name.endswith(self.image_suffix): 
                self.file_names.append(file_name)
        self.file_index = 0
        if len(self.file_names) > 0:
            image_info_path = os.path.join(self.root_dir, self.image_info_result_name)
            if os.path.exists(image_info_path):
                self.load_image_info(image_info_path)
            self.show_image_info(self.file_index)
    
    def last_image(self):
        if len(self.file_names) < 1: return
        self.update_image_info(self.file_index)
        if self.file_index > 0:
            self.file_index -= 1
            self.show_image_info(self.file_index)

    def next_image(self):
        if len(self.file_names) < 1: return
        self.update_image_info(self.file_index)
        if self.file_index < len(self.file_names) - 1:
            self.file_index += 1
            self.show_image_info(self.file_index)

    def show_image_info(self, index):
        file_name = self.file_names[index]
        file_path = os.path.join(self.root_dir, file_name)
        self.mat = cv2.imread(file_path)
        width = 0
        height = 0
        self.points = []
        if file_name in self.image_info:
            old_info = self.image_info[file_name]
            width = old_info['width']
            height = old_info['height']
            self.points = old_info['points']
            if len(self.points) > 0 and self.checkBoxSelectPoints.isChecked():
                for (x, y) in self.points:cv2.circle(self.mat, (x, y), 2, (0, 0, 255), 2)
        
        self.spinBoxWidth.setValue(width)
        self.spinBoxHeight.setValue(height)
        self.display_image(self.mat)
        self.label_2.setText(f'Set the image size.  {self.file_index+1}/{len(self.file_names)}')

    def update_image_info(self, index):
        file_name = self.file_names[index]
        
        width = self.spinBoxWidth.value()
        height = self.spinBoxHeight.value()
        image_info = {'width': width, 'height': height, 'points': self.points}
        if file_name not in self.image_info:
            self.image_info[file_name] = image_info
        else:
            old_info = self.image_info[file_name]
            for key in image_info.keys():
                if old_info[key] != image_info[key]:
                    self.image_info[file_name][key] = image_info[key]

    def display_image(self, image):
        height, width, channels = image.shape
        if height > 400 or width > 800:
            self.resize_rate = height / 400 if height / 400 > width / 800 else width / 800
            w = int(width / self.resize_rate)
            h = int(height / self.resize_rate)
            img = cv2.resize(image, (w, h))
        else:
            img = image

        line_bytes = channels * w
        qt_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        label_image: QImage = QImage(qt_image.data, w, h, line_bytes, QImage.Format_RGB888)
        self.label.setPixmap(QPixmap.fromImage(label_image))
        self.left_top = [self.center[0]-w//2, self.center[1]-h//2]
        self.bottom_right = [self.left_top[0]+w, self.left_top[1]+h]

    def mousePressEvent(self, event):
        (x1, y1), (x2, y2) = self.left_top, self.bottom_right
        x, y = event.x(), event.y()

        if not self.checkBoxSelectPoints.isChecked(): return
        if x1<= x < x2 and y1 <= y < y2:
            x = int((x - x1) * self.resize_rate)
            y = int((y - y1) * self.resize_rate)
            self.points.append([x, y])
            if len(self.points) > self.point_nums: self.points.pop(0)
            image_draw = np.array(self.mat)
            for (px, py) in self.points:
                cv2.circle(image_draw, (px, py), 2, (0, 0, 255), 2)
            self.display_image(image_draw)

    def closeEvent(self, *args, **kwargs):
        if len(list(self.image_info.keys())) > 0:
            image_info_path = os.path.join(self.root_dir, self.image_info_result_name)
            self.save_image_info(image_info_path)

    def load_image_info(self, image_info_path):
        with open(image_info_path, 'r') as f:
            self.image_info = ast.literal_eval(f.readline())

    def save_image_info(self, image_info_path):
        with open(image_info_path, 'w') as f:
            f.write(str(self.image_info))



if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MyPS()
    w.show()
    sys.exit(app.exec_())
