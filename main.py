#!/usr/bin/python
#coding:utf-8 

import cv2
import numpy as np
import sys
from PySide2.QtWidgets import QMainWindow, QFileDialog, QApplication
from PySide2.QtGui import QImage, QPixmap
from PySide2.QtCore import Qt

from ui.ui_color_segment import Ui_MainWindow


class MyPS(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.label.setAlignment(Qt.AlignCenter)

        self.fName = ''
        self.center = [450, 335]
        self.left_top = [450, 335]
        self.bottom_right = [451, 336]
        self.mat = np.zeros([1, 1, 3], np.uint8)
        self.resize_rate = 1.0
        self.points = []
        self.point_nums = 2
        
        self.actionOpen.triggered.connect(self.load_file)
        
    def load_file(self):
        self.fName = QFileDialog.getOpenFileName(self, 'Open File', './', 'Image Files (*.png *.jpg *.bmp)')
        if self.fName[0].endswith(('.png', '.jpg', '.bmp')):
            self.mat = cv2.imread(self.fName[0])
            self.display_image(self.mat)
        
    # 使用label显示图片
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
        pass



if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MyPS()
    w.show()
    sys.exit(app.exec_())
