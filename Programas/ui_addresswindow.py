from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QComboBox


class DialogWindow(QDialog):
    def __init__(self, ip = "", user = "", password = "", sourceType = ""):
        super().__init__()
        self.setWindowTitle("Ingreso de Datos")

        # Layout principal
        self.layout = QVBoxLayout()

        # Menú desplegable para seleccionar la opción
        self.option_label = QLabel("Seleccione una opción:")
        self.option_combobox = QComboBox()
        self.option_combobox.addItems(["Camara Integrada", "Camara IP", "Ejemplo"])
        self.option_combobox.setCurrentText(sourceType)
        self.option_combobox.currentIndexChanged.connect(self.update_fields)

        self.layout.addWidget(self.option_label)
        self.layout.addWidget(self.option_combobox)

        # Campo de entrada para IP
        self.ip_label = QLabel("IP:")
        self.ip_input = QLineEdit()
        self.ip_input.setText(ip)
        self.layout.addWidget(self.ip_label)
        self.layout.addWidget(self.ip_input)

        # Campo de entrada para Usuario
        self.user_label = QLabel("Usuario:")
        self.user_input = QLineEdit()
        self.user_input.setText(user)
        self.layout.addWidget(self.user_label)
        self.layout.addWidget(self.user_input)

        # Campo de entrada para Contraseña
        self.password_label = QLabel("Contraseña:")
        self.password_input = QLineEdit()
        self.password_input.setText(password)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.layout.addWidget(self.password_label)
        self.layout.addWidget(self.password_input)

        # Botones de aceptar y cancelar
        self.button_layout = QHBoxLayout()
        self.accept_button = QPushButton("Aceptar")
        self.cancel_button = QPushButton("Cancelar")
        self.button_layout.addWidget(self.accept_button)
        self.button_layout.addWidget(self.cancel_button)
        self.layout.addLayout(self.button_layout)

        # Conectar botones a funciones
        self.accept_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        # Establecer el layout principal
        self.setLayout(self.layout)

        # Actualizar los campos basándose en la opción seleccionada por defecto
        self.update_fields()

    def get_inputs(self):
        return self.option_combobox.currentText(), self.ip_input.text(), self.user_input.text(), self.password_input.text()

    def update_fields(self):
        option = self.option_combobox.currentText()
        if option == "Camara Integrada":
            self.set_fields_enabled(False)
        elif option == "Camara IP":
            self.set_fields_enabled(True)
        elif option == "Ejemplo":
            self.set_fields_enabled(False)


    def set_fields_enabled(self, enabled):
        if enabled:
            self.ip_input.setStyleSheet("background-color: rgb(255, 255, 255);\n")
            self.user_input.setStyleSheet("background-color: rgb(255, 255, 255);\n")
            self.password_input.setStyleSheet("background-color: rgb(255, 255, 255);\n")

        else:
            self.ip_input.setStyleSheet("background-color: rgb(100, 100, 100);\n")
            self.user_input.setStyleSheet("background-color: rgb(100, 100, 100);\n")
            self.password_input.setStyleSheet("background-color: rgb(100, 100, 100);\n")
        self.ip_input.setEnabled(enabled)
        self.user_input.setEnabled(enabled)
        self.password_input.setEnabled(enabled)


