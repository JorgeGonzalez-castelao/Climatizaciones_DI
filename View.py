import sys

from PyQt6.QtWidgets import QMainWindow, QApplication, QHBoxLayout, QWidget, QLineEdit, QPushButton, QLabel, \
    QVBoxLayout, QCheckBox

from Controller import Controller


class View(QMainWindow):
    def __init__(self):
        super().__init__()
        self.controller = Controller()
        self.contenedorPrincipal = QVBoxLayout()

        # inicializamos la ventana de login y la mostramos
        self.ventanaLogin = self.logginView()
        self.ventanaLogin.show()
        self.contenedorPrincipal.addWidget(self.ventanaLogin)

        # creamos un contenedor para la caja
        container = QWidget()
        container.setLayout(self.contenedorPrincipal)
        # añadimos el contenedor a la ventana y la mostramos
        self.setCentralWidget(container)
        self.setFixedSize(800,500)
        self.show()
    def logginView(self):
        box = QVBoxLayout()


        user = QLineEdit()
        user.setPlaceholderText("Usuario")
        password = QLineEdit()
        password.setPlaceholderText("Contraseña")

        # creamos los elementos que contienen los parametros para registrarse
        self.nombre = QLineEdit()
        self.nombre.setPlaceholderText("Nombre")
        self.apellido = QLineEdit()
        self.apellido.setPlaceholderText("Apellido")
        self.direccion = QLineEdit()
        self.direccion.setPlaceholderText("Dirección")
        self.telefono = QLineEdit()
        self.telefono.setPlaceholderText("Teléfono")
        self.admin = QCheckBox("Administrador")


        # creamos una caja para los botones
        buttonsBox = QHBoxLayout()
        # botón para iniciar sesión
        self.bLogin = QPushButton("Iniciar Sesión")
        self.bLogin.pressed.connect(lambda: self.on_loggin_pressed(self.bLogin.text(), user.text(), password.text(), self.nombre.text(), self.apellido.text(), self.direccion.text(), self.telefono.text(), self.admin.isChecked()))
        # botón para registrarse
        self.bRegister = QPushButton("Registrarse")
        self.bRegister.pressed.connect(self.on_register_pressed)

        # añadimos los botones a la caja
        buttonsBox.addWidget(self.bLogin)
        buttonsBox.addWidget(self.bRegister)

        box.addWidget(user)
        box.addWidget(password)

        box.addWidget(self.nombre)
        box.addWidget(self.apellido)
        box.addWidget(self.direccion)
        box.addWidget(self.telefono)
        box.addWidget(self.admin)

        box.addLayout(buttonsBox)
        container = QWidget()
        container.setLayout(box)
        self.hide_show_register()
        return container


    def productsView(self):
        box = QHBoxLayout()
        text = QLabel("Bienvenido")
        box.addWidget(text)
        container = QWidget()
        container.setLayout(box)
        return container


    def on_loggin_pressed(self, text, username, password, nombre, apellido, direccion, telefono, admin):
        if text == "Iniciar Sesión":
            print("Iniciar Sesión")
            if self.controller.consultar_cliente(username, password):
                self.changeToLoggedView()

        else:
            print("Registrarse")
            self.controller.insertar_cliente(username, password, nombre, apellido, direccion, telefono, admin)
            self.changeToLoggedView()


    def changeToLoggedView(self):
        self.ventanaLogin.hide()
        self.ventanaLogged = self.productsView()
        self.ventanaLogged.show()
        self.contenedorPrincipal.addWidget(self.ventanaLogged)

    def on_register_pressed(self):
        if self.bRegister.text() == "Registrarse":
            self.bRegister.setText("Inicio de Sesión")
            self.bLogin.setText("Crear Usuario")
            self.hide_show_register()
        else:
            self.bRegister.setText("Registrarse")
            self.bLogin.setText("Iniciar Sesión")
            self.hide_show_register()

    def hide_show_register(self):
        if self.bRegister.text() == "Registrarse":
            self.nombre.hide()
            self.apellido.hide()
            self.direccion.hide()
            self.telefono.hide()
            self.admin.hide()
        else:
            self.nombre.show()
            self.apellido.show()
            self.direccion.show()
            self.telefono.show()
            self.admin.show()



if __name__ == "__main__":
    aplicacion = QApplication(sys.argv)
    ventana = View()
    aplicacion.exec()