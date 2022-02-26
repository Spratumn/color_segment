# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'color_segmentFcWqwg.ui'
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
        self.actionMethod1 = QAction(MainWindow)
        self.actionMethod1.setObjectName(u"actionMethod1")
        self.actionMethod2 = QAction(MainWindow)
        self.actionMethod2.setObjectName(u"actionMethod2")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 900, 23))
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName(u"menu")
        self.menuSegment = QMenu(self.menubar)
        self.menuSegment.setObjectName(u"menuSegment")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menuSegment.menuAction())
        self.menu.addAction(self.actionOpen)
        self.menu.addAction(self.actionExit)
        self.menuSegment.addAction(self.actionMethod1)
        self.menuSegment.addAction(self.actionMethod2)

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
        self.actionMethod1.setText(QCoreApplication.translate("MainWindow", u"Method1", None))
        self.actionMethod2.setText(QCoreApplication.translate("MainWindow", u"Method2", None))
        self.label.setText("")
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuSegment.setTitle(QCoreApplication.translate("MainWindow", u"Segment", None))
    # retranslateUi

