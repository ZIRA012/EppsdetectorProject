# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'video.ui'
#
# Created by: PyQ65 UI code generator 5.14.1 #migrado  a pyqt6
#
# WARNING! All changes made in this file will be lost!

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import cv2
import sys
from PyQt6.QtWidgets import QFileDialog
from ultralytics import YOLO
from sort import *

from ultralytics import YOLO
csv_file = "C:/Users/Ronald/Anheuser-Busch InBev/TECH - DetecionEpps/reporte.csv"
classNames = ['CASCO', 'MASCARA', 'SIN CASCO', 'SIN MASCARA', 'SIN CHALECO', 'PERSONA', 'CONO DE SEGURIDAD',
              'CHALECO', 'maquinaria', 'VEHICULO']
model = YOLO('ppe.pt')

class Ui_MainWindow(object):



    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 650)
        MainWindow.setMinimumSize(QtCore.QSize(900, 530))
        MainWindow.setMaximumSize(QtCore.QSize(900, 530))
        MainWindow.setStyleSheet("QWidget#centralwidget{background-color: rgb(224, 224, 224);}\n"
"")



        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")


        self.output_img = QtWidgets.QLabel(self.centralwidget)
        self.output_img.setGeometry(QtCore.QRect(0, 50, 640, 480))
        self.output_img.setStyleSheet("background-color: rgb(64, 64, 64);")
        self.output_img.setText("")
        self.output_img.setObjectName("label")

############################################### GRAFICOS ########################################################################
        self.mainTitle = QtWidgets.QLabel(self.centralwidget)
        self.mainTitle.setGeometry(QtCore.QRect(0, 0, 900, 50))
        self.mainTitle.setStyleSheet("font: 20pt \"Fira code\";\n"
                                     "background-color: rgb(240, 236, 236);\n"
                                     "border-bottom: 2px solid black;\n"
                                     "")
        self.mainTitle.setObjectName("label_2")

        self.logoTech = QtWidgets.QLabel(self.centralwidget)
        self.logoTech.setGeometry(QtCore.QRect(0, 0, 201, 50))
        self.pixmap = QPixmap("../tech.png")
        self.logoTech.setPixmap(self.pixmap)
        self.logoTech.setObjectName("logoTech")

#################################################################BOTONES##########################################################################################
        self.stopButton = QtWidgets.QPushButton(self.centralwidget)
        self.stopButton.setGeometry(QtCore.QRect(658, 480, 231, 41))
        self.stopButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.stopButton.setStyleSheet("border-radius:20px;\n"
"background-color: rgb(255, 51, 51);")
        self.stopButton.setObjectName("stopButton")



        self.startButton = QtWidgets.QPushButton(self.centralwidget)
        self.startButton.setGeometry(QtCore.QRect(658, 430, 231, 41))
        self.startButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.startButton.setStyleSheet("border-radius:20px;\n"
"background-color: rgb(0, 204, 0);\n"
"\n"
"")
        self.startButton.setObjectName("startButton")



        self.exitButton = QtWidgets.QPushButton(self.centralwidget)
        self.exitButton.setGeometry(QtCore.QRect(808, 5, 90, 40))
        self.exitButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.exitButton.setStyleSheet("border-radius:5px;\n"
"background-color: rgb(169, 169, 169);")
        self.exitButton.setObjectName("exitButton")


        self.browseButton = QtWidgets.QPushButton(self.centralwidget)
        self.browseButton.setGeometry(QtCore.QRect(600,70,90,25))
        self.browseButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.browseButton.setStyleSheet("border-radius:4px;\n"
"background-color: rgb(169, 169, 169);")
        self.browseButton.setObjectName("browseButton")





        MainWindow.setCentralWidget(self.centralwidget)


        self.stopButton.clicked.connect(self.cancel)
        self.startButton.clicked.connect(self.start_video)
        self.exitButton.clicked.connect(self.exit)
        self.browseButton.clicked.connect(self.browser)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def start_video(self):
        self.Work = Work()
        self.Work.start()
        self.Work.Imageupd.connect(self.Imageupd_slot)

    def Imageupd_slot(self, Image):
        self.output_img.setPixmap(QPixmap.fromImage(Image))

    def cancel(self):
        self.output_img.clear()
        self.Work.stop()

    def browser(self):
        # Mostrar el diálogo de selección de archivo
        xdfile,_ = QFileDialog.getOpenFileName(None, 'open file', '', 'All files (*)')
        if xdfile:
            print(xdfile)




    def exit(self):
        sys.exit()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Prueba"))
        self.stopButton.setText(_translate("MainWindow", "Detener"))
        self.startButton.setText(_translate("MainWindow", "Iniciar"))
        self.exitButton.setText(_translate("MainWindow", "Salir"))
        self.mainTitle.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">SISTEMA DE DETECCION DE EPPS</p></body></html>"))


cap = cv2.VideoCapture()
class Work(QThread):
    Imageupd = pyqtSignal(QImage)
    def __init__(self):
        super().__init__()
        self.thread_running = True
        self.trackerHead = Sort(max_age=20, min_hits=12, iou_threshold=0.3)
        self.trackerVet = Sort(max_age=20, min_hits=12, iou_threshold=0.3)
        self.Detected_Head = []
        self.Detected_Vet = []


    def run(self):
        cap.open("../video1.mp4")
        while self.thread_running:
            success, img = cap.read()
            if success:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                flip = cv2.flip(img, 1)
                convertir_QT = QImage(flip.data, flip.shape[1], flip.shape[0], QImage.Format.Format_RGB888)
                pic = convertir_QT.scaled(640, 480, Qt.AspectRatioMode.KeepAspectRatio)
                self.Imageupd.emit(pic)
                cv2.waitKey(100)
        cap.release()
    def stop(self):
        cap.release()
        self.thread_running = False
        self.quit()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
