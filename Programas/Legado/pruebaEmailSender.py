from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow
import sys
from PyQt6.QtCore import QThread, pyqtSignal
from emailsender import sentEmail

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 650)
        MainWindow.setMinimumSize(QtCore.QSize(900, 530))
        MainWindow.setMaximumSize(QtCore.QSize(900, 530))
        MainWindow.setStyleSheet("QWidget#centralwidget{background-color: rgb(224, 224, 224);}\n""")

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.output_img = QtWidgets.QLabel(self.centralwidget)
        self.output_img.setGeometry(QtCore.QRect(0, 50, 640, 480))
        self.output_img.setStyleSheet("background-color: rgb(64, 64, 64);")
        self.output_img.setText("")
        self.output_img.setObjectName("label")

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

        self.stopButton = QtWidgets.QPushButton(self.centralwidget)
        self.stopButton.setGeometry(QtCore.QRect(658, 480, 231, 41))
        self.stopButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.stopButton.setStyleSheet("border-radius:12px;\n"
                                      "background-color: rgb(169, 169, 169);")
        self.stopButton.setObjectName("stopButton")
        self.stopButton.setEnabled(True)
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Prueba"))
        self.stopButton.setText(_translate("MainWindow", "Detener"))
        self.mainTitle.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">SISTEMA DE DETECCION DE EPPS</p></body></html>"))



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.stopButton.clicked.connect(self.start)

    def start(self):
        self.sendEmail = sentEmail("eppsdetector@outlook.com", "Pepsi2024.","manteca012@gmail.com", "esto es un email de prueba", "Mensaje de prueba", "Image.jpg")
        self.sendEmail.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


