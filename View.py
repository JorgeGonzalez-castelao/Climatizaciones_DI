import sys

from PyQt6.QtWidgets import QMainWindow, QApplication, QHBoxLayout, QWidget, QLineEdit, QPushButton, QLabel, \
    QVBoxLayout, QCheckBox, QComboBox

from Cliente import Cliente
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
        self.productbuy = []
        box = QVBoxLayout()
        print(self.cliente)
        if self.cliente.admin:
            bCreateProduct = QPushButton("Crear Producto")
            box2 = QHBoxLayout()
            nombre = QLineEdit()
            nombre.setPlaceholderText("Nombre")
            descripcion = QLineEdit()
            descripcion.setPlaceholderText("Descripción")
            precio = QLineEdit()
            precio.setPlaceholderText("Precio")
            box2.addWidget(nombre)
            box2.addWidget(descripcion)
            box2.addWidget(precio)
            bCreateProduct.pressed.connect(lambda: self.createProduct(nombre.text(), descripcion.text(), precio.text()))
            box.addLayout(box2)
            box.addWidget(bCreateProduct)
        self.comboProductos = QComboBox()
        self.comboProductos.addItem("")
        print("Consultar productos")
        productos = self.controller.consultar_producto_servicio()
        for producto in productos:
            print(producto)
            texto = producto[0] + ", " + str(producto[2]) + "€"
            self.comboProductos.addItem(texto)
        boxPedido = QHBoxLayout()
        boxPedido.addWidget(self.comboProductos)
        self.cantidad = QLineEdit()
        self.cantidad.setPlaceholderText("Cantidad")
        boxPedido.addWidget(self.cantidad)
        box.addLayout(boxPedido)
        bAddProduct = QPushButton("Añadir Producto")
        bAddProduct.pressed.connect(lambda: self.addProduct(self.comboProductos.currentText(), self.cantidad.text()))
        box.addWidget(bAddProduct)
        self.labelProductosComprar = QLabel("Productos en la cesta: ")
        box.addWidget(self.labelProductosComprar)
        btnComprar = QPushButton("Comprar")
        btnComprar.pressed.connect(lambda: self.on_comprar_pressed())
        box.addWidget(btnComprar)
        btnCompras = QPushButton("Ver Compras")
        btnCompras.pressed.connect(lambda: self.changeToSeeBoughts())
        box.addWidget(btnCompras)
        container = QWidget()
        container.setLayout(box)
        return container

    def on_comprar_pressed(self):
        print(self.cliente.username + " va a comprar: " + str(self.productbuy))
        self.controller.insertar_compra(self.cliente.username, self.productbuy)
        self.labelProductosComprar.setText("Productos en la cesta: ")
        self.productbuy = []

    def addProduct(self, item, cantidad):
        item = item.split(",")
        self.productbuy.append((item[0], item[1],cantidad))
        print(self.productbuy)
        self.comboProductos.setCurrentIndex(0)
        self.cantidad.clear()
        self.labelProductosComprar.setText(self.labelProductosComprar.text() + "\n " + item[0] + ", " + str(cantidad) + " unidades, " + str(item[1]) + " = " + str(int(cantidad) * float(item[1].split("€")[0])) + "€")

    def createProduct(self, nombre, descripcion, precio):
        print("Crear Producto")
        self.controller.insertar_producto_servicio(nombre, descripcion, precio)
        self.comboProductos.addItem(nombre + ", " + str(precio) + "€")

    def on_loggin_pressed(self, text, username, password, nombre, apellido, direccion, telefono, admin):
        if text == "Iniciar Sesión":
            print("Iniciar Sesión")
            if self.controller.consultar_cliente(username, password):
                self.cliente = self.controller.get_cliente(username)
                self.changeToLoggedView("Log in")
        else:
            print("Registrarse")
            self.controller.insertar_cliente(username, password, nombre, apellido, direccion, telefono, admin)
            self.cliente = self.controller.get_cliente(username)
            self.changeToLoggedView("Log in")


    def changeToLoggedView(self, proveniente):
        if proveniente == "Log in":
            self.ventanaLogin.hide()
            self.ventanaLogged = self.productsView()
            self.ventanaLogged.show()
            self.contenedorPrincipal.addWidget(self.ventanaLogged)
        elif proveniente == "Compras":
            self.ventanaCompras.hide()
            self.ventanaLogged = self.productsView()
            self.ventanaLogged.show()
            self.contenedorPrincipal.addWidget(self.ventanaLogged)
    def seeBoughtsView(self):
        box = QVBoxLayout()
        compras = self.controller.consultar_compra(self.cliente.username)
        label = QLabel("Compras: \n")
        for compra in compras:
            label.setText(label.text() + compra[1] + "\n")
        box.addWidget(label)
        botonVolver = QPushButton("Ir a comprar")
        botonVolver.pressed.connect(lambda: self.changeToLoggedView("Compras"))
        box.addWidget(botonVolver)
        container = QWidget()
        container.setLayout(box)
        return container

    def changeToSeeBoughts(self):
        self.ventanaLogged.hide()
        print("Cambiando a la vista de compras")
        self.ventanaCompras = self.seeBoughtsView()
        self.ventanaCompras.show()
        self.contenedorPrincipal.addWidget(self.ventanaCompras)

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