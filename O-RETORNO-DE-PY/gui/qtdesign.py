from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from ksignalplotter import KSignalPlotter


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1079, 635)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.ksignalplotter = KSignalPlotter(self.centralwidget)
        self.ksignalplotter.setObjectName(u"ksignalplotter")
        self.ksignalplotter.setGeometry(QRect(560, 20, 491, 171))
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
    # retranslateUi
