from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QDialog, QDialogButtonBox

class EmailDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Ingresar Correo Electrónico")

        layout = QVBoxLayout()

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Ingrese su correo electrónico")
        layout.addWidget(self.email_input)

        self.info_label = QLabel("El primer correo puede entrar en la carpeta de spam.")
        self.info_label.setStyleSheet('font: 8pt \"Fira code\";\n')
        layout.addWidget(self.info_label)

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)

        self.setLayout(layout)

    def get_email(self):
        return self.email_input.text()







