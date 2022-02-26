#!/usr/bin/python
#coding:utf-8 

import cv2
import numpy as np
import sys
from PySide2.QtWidgets import QMainWindow, QMessageBox, QFileDialog, QApplication
from PySide2.QtGui import QImage, QPixmap
from PySide2.QtCore import Qt

from ui.ui_color_segment import Ui_MainWindow
from color_segment import color_segment_1, color_segment_2, save_result_to_txt


# 主窗口类，继承窗口Ui_MainWindow主界面
class MyPS(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 窗口属性修改
        self.label.setAlignment(Qt.AlignCenter)

        # 实例属性初始化
        self.fName = ''
        self.mat = np.zeros([1, 1, 3], np.uint8)
        # 信号槽连接
        self.actionOpen.triggered.connect(self.load_file)
        self.actionMethod1.triggered.connect(self.color_segment1)
        self.actionMethod2.triggered.connect(self.color_segment2)
        self.method = 1

    def color_segment1(self):
        rects = color_segment_1(self.mat)
        image = self.draw_rects(rects, np.array(self.mat))
        self.display_image(image)

    def color_segment2(self):
        rects = color_segment_2(self.mat)
        image = self.draw_rects(rects, np.array(self.mat))
        self.display_image(image)
        
    def draw_rects(self, rects, image):
        for (x1, y1, x2, y2) in rects:
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), 2)
        return image


    # 加载文件,根据后缀判断文件类型
    def load_file(self):
        self.fName = QFileDialog.getOpenFileName(self, 'Open File', './',
                                                 'Image Files (*.png *.jpg *.bmp)')
        if self.fName[0].endswith(('.png', '.jpg', '.bmp')):
            self.mat = cv2.imread(self.fName[0])
            self.display_image(self.mat)
        
    # 使用label显示图片
    def display_image(self, image):
        height, width, channels = image.shape
        if height > 400 or width > 800:
            rate = height / 400 if height / 400 > width / 800 else width / 800
            width = int(width / rate)
            height = int(height / rate)
            img = cv2.resize(image, (width, height))
        else:
            img = image
        self.statusbar.showMessage('img size:({},{})'.format(width, height))
        self.statusbar.show()
        line_bytes = channels * width
        qt_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        label_image: QImage = QImage(qt_image.data, width, height, line_bytes, QImage.Format_RGB888)
        self.label.setPixmap(QPixmap.fromImage(label_image))

    def mousePressEvent(self, event):
        print('clicked at (', event.x(), ',', event.y(), ')')

    def closeEvent(self, *args, **kwargs):
        pass



if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MyPS()
    w.show()
    sys.exit(app.exec_())
