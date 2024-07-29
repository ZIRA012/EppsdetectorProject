import sys
from PyQt6 import QtGui, QtWidgets
from PyQt6.QtWidgets import QFileDialog, QApplication, QMainWindow, QMessageBox
from ui_mainwindow import Ui_MainWindow
from ui_addresswindow import DialogWindow
import os
from thread_video import Work
from config_manager import load_config, save_config, modify_config
from emailsender import sendEmail
from ui_emailwindow import EmailDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Ruta predeterminada

        self.config = load_config("config.json")

        #cargo de configuraciones por defecto
        self.default_path_csv = self.config.get("default_path_csv", "")  # Cambia esto a la ruta que desees
        self.videoSource = self.config.get("videoSource", "")
        self.sourceType = self.config.get("sourceType", "")
        self.ip = self.config.get("ip", "")
        self.user = self.config.get("user", "")
        self.password = self.config.get("password", "")
        self.emailRecipient = self.config.get("emailRecipient", "")

        self.sending_email = False

        self.ui.filePathLabel.setText(f"{os.path.basename(self.default_path_csv)}")
        self.ui.sourceType.setText(self.sourceType)
        self.ui.email.setText(self.emailRecipient)
        # Conectar los botones a sus funciones
        self.ui.stopButton.clicked.connect(self.cancel)
        self.ui.startButton.clicked.connect(self.start_video)
        self.ui.exitButton.clicked.connect(self.exit)
        self.ui.browseButton.clicked.connect(self.browser)
        self.ui.addressButton.clicked.connect(self.open_address_window)
        self.ui.emailButton.clicked.connect(self.change_email)

    def start_video(self):
        if self.default_path_csv.endswith(".csv"):
            self.ui.startButton.setEnabled(False)
            self.ui.startButton.setStyleSheet("background-color: rgb(169, 169, 169);\n"
                                              "border-radius:12px;\n")
            self.ui.stopButton.setEnabled(True)
            self.ui.stopButton.setStyleSheet("background-color: rgb(255, 51, 51);\n"
                                             "border-radius:12px;\n")
            self.Work = Work(self.default_path_csv, self.sourceType, self.videoSource,
                             self.ui.emailCheckbox.isChecked())
            self.Work.start()
            self.Work.detected_signal.connect(self.send_email_threaded)
            self.Work.Imageupd.connect(self.Imageupd_slot)
            self.Work.finished.connect(self.on_work_finished)
            self.Work.errorReading.connect(self.error_reading_source)

        else:
            self.browser()

    def send_email_threaded(self, message, imgPath):
        if not self.sending_email:
            self.sending_email = True
            self.email_thread = sendEmail("eppsdetector@outlook.com", "Pepsi2024.", self.emailRecipient, "PRUEBA",
                                          message, imgPath)
            self.email_thread.finished.connect(self.reset_sending_email)
            self.email_thread.start()

    def reset_sending_email(self):
        self.sending_email = False

    def on_work_finished(self):
        # Habilitar el botón de "Start" y deshabilitar "Stop" cuando el hilo termine
        self.ui.startButton.setEnabled(True)
        self.ui.startButton.setStyleSheet("background-color: rgb(0, 204, 0);\n"
                                          "border-radius:12px;\n")
        self.ui.stopButton.setEnabled(False)
        self.ui.stopButton.setStyleSheet("background-color: rgb(169, 169, 169);\n"
                                         "border-radius:12px;\n")

    def Imageupd_slot(self, Image):
        self.ui.output_img.setPixmap(QtGui.QPixmap.fromImage(Image))

    def error_reading_source(self, errorText=""):
        error_dialog = QtWidgets.QMessageBox()
        error_dialog.setIcon(QtWidgets.QMessageBox.Icon.Critical)
        error_dialog.setText(errorText)
        error_dialog.setWindowTitle("Error")
        error_dialog.exec()

    def cancel(self):
        self.ui.output_img.clear()
        if hasattr(self, 'Work') and self.Work.isRunning():
            self.Work.stop()
        else:
            print("ningun hilo fue iniciado")

    def browser(self):
        # Mostrar el diálogo de selección de archivo
        file, _ = QFileDialog.getOpenFileName(self, "Seleccionar Archivo CSV", self.default_path_csv,
                                              "Archivos CSV (*.csv)")
        if file:
            if file.endswith('.csv'):
                self.default_path_csv = file
                modify_config(self.config, "default_path_csv", self.default_path_csv)
                save_config("config.json", self.config)
                print("Archivo CSV seleccionado:", os.path.basename(self.default_path_csv))
                self.ui.filePathLabel.setText(f"{os.path.basename(self.default_path_csv)}")
            else:
                QMessageBox.warning(self, "Error de Archivo", "Por favor seleccione un archivo CSV.")

    def open_address_window(self):
        dialog = DialogWindow(self.ip, self.user, self.password, self.sourceType)
        if dialog.exec():
            option, ip, user, password = dialog.get_inputs()
            if option == "Camara Integrada":
                print(f"Cámara Integrada seleccionada: retorna 0{option}")
            elif option == "Camara IP":
                self.ip = ip
                self.user = user
                self.password = password
                modify_config(self.config, "ip", self.ip)
                modify_config(self.config, "user", self.user)
                modify_config(self.config, "password", self.password)
                print(f"http://{user}:{password}@{ip}/ISAPI/Streaming/channels/102/httpPreview")
                self.videoSource = (f"http://{user}"
                                    f":{password}@{ip}/ISAPI/Streaming/channels/102/httpPreview")
                modify_config(self.config, "videoSource", self.videoSource)
            elif option == "Ejemplo":
                print("Ejemplo seleccionado: retorna 'video.mp4'")
                self.videoSource = "Extension15fps.mp4"
                modify_config(self.config, "videoSource", self.videoSource)
            self.sourceType = option
            self.ui.sourceType.setText(option)
            modify_config(self.config, "sourceType", self.sourceType)
            save_config("config.json", self.config)

    def change_email(self):
        dialog = EmailDialog()
        if dialog.exec():
            self.emailRecipient = dialog.get_email()
            modify_config(self.config, "emailRecipient", self.emailRecipient)
            save_config("config.json", self.config)
            self.ui.email.setText(self.emailRecipient)

    def exit(self):
        sys.exit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
