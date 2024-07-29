from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget
import sys


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
        self.pixmap = QPixmap("tech.png")
        self.logoTech.setPixmap(self.pixmap)
        self.logoTech.setObjectName("logoTech")

        self.stopButton = QtWidgets.QPushButton(self.centralwidget)
        self.stopButton.setGeometry(QtCore.QRect(658, 480, 231, 41))
        self.stopButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.stopButton.setStyleSheet("border-radius:12px;\n"
                                      "background-color: rgb(169, 169, 169);")
        self.stopButton.setObjectName("stopButton")
        self.stopButton.setEnabled(False)

        self.startButton = QtWidgets.QPushButton(self.centralwidget)
        self.startButton.setGeometry(QtCore.QRect(658, 430, 231, 41))
        self.startButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.startButton.setStyleSheet("border-radius:12px;\n"
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
        self.browseButton.setGeometry(QtCore.QRect(806, 104, 80, 18))
        self.browseButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.browseButton.setStyleSheet("border-radius:4px;\n"
                                        "background-color: rgb(169, 169, 169);")
        self.browseButton.setObjectName("browseButton")

        self.addressButton = QtWidgets.QPushButton(self.centralwidget)
        self.addressButton.setGeometry(QtCore.QRect(806, 178, 80, 18))
        self.addressButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.addressButton.setStyleSheet("border-radius:4px;\n"
                                         "background-color: rgb(169, 169, 169);")
        self.addressButton.setObjectName("browseButton")

        self.filePathLabel = QtWidgets.QLabel(self.centralwidget)
        self.filePathLabel.setGeometry(QtCore.QRect(650, 104, 140, 18))
        self.filePathLabel.setObjectName("filePathLabel")
        self.filePathLabel.setStyleSheet("background-color: rgb(255,255, 255);\n"
                                         "font-size: 10pt;\n"
                                         "border-bottom: 1px solid black;")
        self.filePathLabel.setText("")

        self.dataLabelTitle = QtWidgets.QLabel(self.centralwidget)
        self.dataLabelTitle.setGeometry(QtCore.QRect(740, 60, 90, 20))
        self.dataLabelTitle.setStyleSheet("font: 12pt \"Fira code\";\n")
        self.dataLabelTitle.setObjectName("dataLabel")

        self.dataLabel = QtWidgets.QLabel(self.centralwidget)
        self.dataLabel.setGeometry(QtCore.QRect(650, 84, 90, 20))
        self.dataLabel.setStyleSheet("font: 10pt \"Fira code\";\n")
        self.dataLabel.setObjectName("dataLabel")

        self.sourceType = QtWidgets.QLabel(self.centralwidget)
        self.sourceType.setGeometry(QtCore.QRect(650, 178, 150, 18))
        self.sourceType.setObjectName("filePathLabel")
        self.sourceType.setStyleSheet("background-color: rgb(255,255, 255);\n"
                                       "font-size: 10pt;\n"
                                       "border-bottom: 1px solid black;")
        self.sourceType.setText("")

        self.sourceTitle = QtWidgets.QLabel(self.centralwidget)
        self.sourceTitle.setGeometry(QtCore.QRect(730, 136, 90, 20))
        self.sourceTitle.setStyleSheet("font: 12pt \"Fira code\";\n")
        self.sourceTitle.setObjectName("fuente")
        self.sourceTitle.setText("FUENTE")

        self.sourceLabel = QtWidgets.QLabel(self.centralwidget)
        self.sourceLabel.setGeometry(QtCore.QRect(650, 160, 90, 20))
        self.sourceLabel.setStyleSheet("font: 10pt \"Fira code\";\n")
        self.sourceLabel.setObjectName("dataLabel")
        self.sourceLabel.setText("Tipo:")

        self.alertsTitle = QtWidgets.QLabel(self.centralwidget)
        self.alertsTitle.setGeometry(QtCore.QRect(730, 210, 90, 20))
        self.alertsTitle.setStyleSheet("font: 12pt \"Fira code\";\n")
        self.alertsTitle.setObjectName("fuente")
        self.alertsTitle.setText("ALERTAS")

        self.emailButton = QtWidgets.QPushButton(self.centralwidget)
        self.emailButton.setGeometry(QtCore.QRect(806, 274, 80, 20))
        self.emailButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.emailButton.setStyleSheet("border-radius:4px;\n"
                                        "background-color: rgb(169, 169, 169);")
        self.emailButton.setObjectName("browseButton")
        self.emailButton.setText("Cambiar")

        # Declaración del QCheckBox
        self.emailCheckbox = QtWidgets.QCheckBox(self.centralwidget)
        self.emailCheckbox.setGeometry(QtCore.QRect(650, 230, 90, 20))
        self.emailCheckbox.setStyleSheet("font: 10pt \"Fira code\";")
        self.emailCheckbox.setObjectName("emailCheckbox")
        self.emailCheckbox.setText("Enviar Email")

        self.emailLabel = QtWidgets.QLabel(self.centralwidget)
        self.emailLabel.setGeometry(QtCore.QRect(650, 254, 90, 20))
        self.emailLabel.setStyleSheet("font: 10pt \"Fira code\";\n")
        self.emailLabel.setObjectName("dataLabel")
        self.emailLabel.setText("Correo:")

        self.email = QtWidgets.QLabel(self.centralwidget)
        self.email.setGeometry(QtCore.QRect(650, 274, 150, 18))
        self.email.setObjectName("filePathLabel")
        self.email.setStyleSheet("background-color: rgb(255,255, 255);\n"
                                       "font-size: 10pt;\n"
                                 "border-bottom: 1px solid black;")
        self.email.setText("")


        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Prueba"))
        self.stopButton.setText(_translate("MainWindow", "Detener"))
        self.startButton.setText(_translate("MainWindow", "Iniciar"))
        self.exitButton.setText(_translate("MainWindow", "Salir"))
        self.mainTitle.setText(_translate("MainWindow",
                                          "<html><head/><body><p align=\"center\">SISTEMA DE DETECCION DE EPPS</p></body></html>"))
        self.browseButton.setText(_translate("MainWindow", "Seleccionar"))
        self.addressButton.setText(_translate("MainWindow", "Fuente"))
        self.dataLabelTitle.setText("DATOS")
        self.dataLabel.setText("Archivo:")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
