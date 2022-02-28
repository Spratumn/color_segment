# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'color_segmentIdoBjz.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(900, 600)
        MainWindow.setMinimumSize(QSize(900, 600))
        MainWindow.setMaximumSize(QSize(900, 600))
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.actionOpen = QAction(MainWindow)
        self.actionOpen.setObjectName(u"actionOpen")
        self.actionOpen.setShortcutContext(Qt.WindowShortcut)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.layoutWidget = QWidget(self.centralwidget)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(8, 9, 927, 571))
        self.gridLayout = QGridLayout(self.layoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.layoutWidget)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(882, 520))
        self.label.setMaximumSize(QSize(882, 520))

        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_4 = QLabel(self.layoutWidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMaximumSize(QSize(40, 23))

        self.gridLayout_2.addWidget(self.label_4, 0, 2, 1, 1)

        self.spinBoxWidth = QSpinBox(self.layoutWidget)
        self.spinBoxWidth.setObjectName(u"spinBoxWidth")
        self.spinBoxWidth.setMaximumSize(QSize(50, 23))
        self.spinBoxWidth.setMaximum(2000)

        self.gridLayout_2.addWidget(self.spinBoxWidth, 0, 3, 1, 1)

        self.pushButtonLast = QPushButton(self.layoutWidget)
        self.pushButtonLast.setObjectName(u"pushButtonLast")
        self.pushButtonLast.setMaximumSize(QSize(40, 23))

        self.gridLayout_2.addWidget(self.pushButtonLast, 0, 6, 1, 1)

        self.checkBoxSelectPoints = QCheckBox(self.layoutWidget)
        self.checkBoxSelectPoints.setObjectName(u"checkBoxSelectPoints")
        self.checkBoxSelectPoints.setMaximumSize(QSize(100, 16777215))

        self.gridLayout_2.addWidget(self.checkBoxSelectPoints, 0, 1, 1, 1)

        self.pushButtonNext = QPushButton(self.layoutWidget)
        self.pushButtonNext.setObjectName(u"pushButtonNext")
        self.pushButtonNext.setMaximumSize(QSize(40, 23))

        self.gridLayout_2.addWidget(self.pushButtonNext, 0, 7, 1, 1)

        self.spinBoxHeight = QSpinBox(self.layoutWidget)
        self.spinBoxHeight.setObjectName(u"spinBoxHeight")
        self.spinBoxHeight.setMaximumSize(QSize(50, 23))
        self.spinBoxHeight.setMaximum(2000)
        self.spinBoxHeight.setSingleStep(1)
        self.spinBoxHeight.setStepType(QAbstractSpinBox.DefaultStepType)
        self.spinBoxHeight.setDisplayIntegerBase(10)

        self.gridLayout_2.addWidget(self.spinBoxHeight, 0, 5, 1, 1)

        self.label_3 = QLabel(self.layoutWidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMaximumSize(QSize(42, 23))

        self.gridLayout_2.addWidget(self.label_3, 0, 4, 1, 1)

        self.label_2 = QLabel(self.layoutWidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(400, 0))
        self.label_2.setMaximumSize(QSize(400, 23))

        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 1)


        self.gridLayout.addLayout(self.gridLayout_2, 1, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 900, 23))
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName(u"menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu.menuAction())
        self.menu.addAction(self.actionOpen)
        self.menu.addAction(self.actionExit)

        self.retranslateUi(MainWindow)
        self.actionExit.triggered.connect(MainWindow.close)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.actionOpen.setText(QCoreApplication.translate("MainWindow", u"Open", None))
#if QT_CONFIG(tooltip)
        self.actionOpen.setToolTip(QCoreApplication.translate("MainWindow", u"Open Image", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.actionOpen.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+O", None))
#endif // QT_CONFIG(shortcut)
        self.label.setText("")
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Width:", None))
        self.pushButtonLast.setText(QCoreApplication.translate("MainWindow", u"<", None))
        self.checkBoxSelectPoints.setText(QCoreApplication.translate("MainWindow", u"Select Points", None))
        self.pushButtonNext.setText(QCoreApplication.translate("MainWindow", u">", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Height:", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Set the image size.", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
    # retranslateUi

