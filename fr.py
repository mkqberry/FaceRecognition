# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'fr.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets
import sys
import os
from dataset import Dataset
from recognize import Recognize

class Ui_MainWindow(object):
    def __init__(self):
        self.dataset = Dataset()
        self.number = 0
        self.names = list()
        
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(461, 188)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.labelInput = QtWidgets.QLabel(self.centralwidget)
        self.labelInput.setGeometry(QtCore.QRect(10, 20, 201, 31))
        self.labelInput.setObjectName("labelInput")
        self.textName = QtWidgets.QLineEdit(self.centralwidget)
        self.textName.setGeometry(QtCore.QRect(200, 25, 221, 21))
        self.textName.setObjectName("textName")
        self.buttonTake = QtWidgets.QPushButton(self.centralwidget)
        self.buttonTake.setGeometry(QtCore.QRect(340, 62, 81, 31))
        self.buttonTake.setObjectName("buttonTake")
        self.buttonTrain = QtWidgets.QPushButton(self.centralwidget)
        self.buttonTrain.setGeometry(QtCore.QRect(240, 62, 81, 31))
        self.buttonTrain.setObjectName("buttonChange")
        self.buttonRecognize = QtWidgets.QPushButton(self.centralwidget)
        self.buttonRecognize.setGeometry(QtCore.QRect(340, 110, 81, 31))
        self.buttonRecognize.setObjectName("buttonRecognize")
        self.buttonRecognize.setDisabled(True)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 461, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.buttonTake.clicked.connect(self.take)
        self.buttonRecognize.clicked.connect(self.predict)
        self.buttonTrain.clicked.connect(self.train)
        self.buttonTrain.setDisabled(True)
        self.buttonTake.setEnabled(False)
        self.textName.textChanged.connect(self.makeVisible)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Face Recognize"))
        self.labelInput.setText(_translate("MainWindow", "Tanımlamak istediğiniz yüz için isim girin:"))
        self.buttonTake.setText(_translate("MainWindow", "Fotoğraf Çek"))
        self.buttonRecognize.setText(_translate("MainWindow", "Yüz Tanı"))
        self.buttonTrain.setText(_translate("MainWindow", "Eğit"))
    
    def take(self):
        self.number += 1
        self.names.append(self.textName.text())
        os.makedirs("dataset", exist_ok=True)
        self.buttonTrain.setEnabled(True)
        name = self.textName.text()
        self.dataset.createDataset(name)

    def train(self):
        os.makedirs("trainer", exist_ok=True)
        self.textName.setText("")
        self.textName.setDisabled(True)
        self.buttonTake.setEnabled(False)
        self.buttonTrain.setEnabled(False)
        self.buttonRecognize.setEnabled(True)
        recognize = Recognize(self.number, self.names)
        recognize.toTrain()
    
    def predict(self):
        self.buttonTrain.setEnabled(False)
        self.buttonTake.setEnabled(False)
        self.buttonTrain.setEnabled(False)
        self.buttonRecognize.setEnabled(False)
        recognize = Recognize(self.number, self.names)
        recognize.predict()
    
    def makeVisible(self):
        self.buttonTake.setEnabled(True)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ex = Ui_MainWindow()
    w = QtWidgets.QMainWindow()
    ex.setupUi(w)
    w.show()
    sys.exit(app.exec_())
