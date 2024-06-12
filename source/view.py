import sys
from PyQt6.QtWidgets import QMainWindow, QApplication, QHBoxLayout, QWidget, QLineEdit, QPushButton, QLabel, \
    QVBoxLayout, QCheckBox, QComboBox, QTableView

from Cliente import Cliente
from Controller import Controller
from ModeloTabla import ModeloTaboa
from informe import Informe


class View(QMainWindow):
    def __init__(self):
        super().__init__()
        self.controller = Controller()
        self.contenedorPrincipal = QVBoxLayout()

        # Inicializamos la ventana de login y la mostramos
        self.ventanaLogin = self.logginView()
        self.ventanaLogin.show()
        self.contenedorPrincipal.addWidget(self.ventanaLogin)

        # Creamos un contenedor para la caja
        container = QWidget()
        container.setLayout(self.contenedorPrincipal)

        # Añadimos el contenedor a la ventana y la mostramos
        self.setCentralWidget(container)
        self.setFixedSize(800, 500)
        self.show()

    def logginView(self):
        """
        Configura la vista de inicio de sesión y registro.

        """
        box = QVBoxLayout()
        user = QLineEdit()
        user.setPlaceholderText("Usuario")
        password = QLineEdit()
        password.setPlaceholderText("Contraseña")

        # Creamos los elementos que contienen los parámetros para registrarse
        self.nombre = QLineEdit()
        self.nombre.setPlaceholderText("Nombre")
        self.apellido = QLineEdit()
        self.apellido.setPlaceholderText("Apellido")
        self.direccion = QLineEdit()
        self.direccion.setPlaceholderText("Dirección")
        self.telefono = QLineEdit()
        self.telefono.setPlaceholderText("Teléfono")
        self.admin = QCheckBox("Administrador")

        # Creamos una caja para los botones
        buttonsBox = QHBoxLayout()

        # Botón para iniciar sesión
        self.bLogin = QPushButton("Iniciar Sesión")
        self.bLogin.pressed.connect(lambda: self.on_loggin_pressed(
            self.bLogin.text(), user.text(), password.text(), self.nombre.text(),
            self.apellido.text(), self.direccion.text(), self.telefono.text(), self.admin.isChecked()))

        # Botón para registrarse
        self.bRegister = QPushButton("Registrarse")
        self.bRegister.pressed.connect(self.on_register_pressed)

        # Añadimos los botones a la caja
        buttonsBox.addWidget(self.bLogin)
        buttonsBox.addWidget(self.bRegister)

        # Añadimos los elementos a la caja principal
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
        """
        Configura la vista de productos para el usuario, incluyendo la opción de
        administrar productos si el usuario es administrador.
        """
        self.productbuy = []
        box = QVBoxLayout()
        print(self.cliente)
        if self.cliente.admin:
            # Crear botones para las acciones de administrador
            bCreateProduct = QPushButton("Crear Producto")
            bEditProduct = QPushButton("Editar Producto")
            bDeleteProduct = QPushButton("Borrar Producto")
            bEditProduct.setToolTip(
                "Ponga el nombre del producto (case sensitive) y los nuevos valores en los campos correspondientes")
            bDeleteProduct.setToolTip("Ponga el nombre del producto (case sensitive) que desea borrar")

            # Crear campos de entrada para la información del producto
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

            # Conectar botones con sus funciones correspondientes
            bCreateProduct.pressed.connect(lambda: self.createProduct(nombre.text(), descripcion.text(), precio.text()))
            bEditProduct.pressed.connect(lambda: self.editProduct(nombre.text(), descripcion.text(), precio.text()))
            bDeleteProduct.pressed.connect(lambda: self.deleteProduct(nombre.text()))
            box.addLayout(box2)

            # Añadir los botones a la caja de botones
            boxButtons = QHBoxLayout()
            boxButtons.addWidget(bCreateProduct)
            boxButtons.addWidget(bEditProduct)
            boxButtons.addWidget(bDeleteProduct)
            box.addLayout(boxButtons)

        # Crear combo box para seleccionar productos
        self.comboProductos = QComboBox()
        self.comboProductos.addItem("")
        print("Consultar productos")
        self.addItemsToComboProductos()

        # Crear layout para seleccionar cantidad de productos
        boxPedido = QHBoxLayout()
        boxPedido.addWidget(self.comboProductos)
        self.cantidad = QLineEdit()
        self.cantidad.setPlaceholderText("Cantidad")
        boxPedido.addWidget(self.cantidad)
        box.addLayout(boxPedido)

        # Botón para añadir producto a la cesta
        bAddProduct = QPushButton("Añadir Producto")
        bAddProduct.pressed.connect(lambda: self.addProduct(self.comboProductos.currentText(), self.cantidad.text()))
        box.addWidget(bAddProduct)

        # Etiqueta para mostrar los productos en la cesta
        self.labelProductosComprar = QLabel("Productos en la cesta: ")
        box.addWidget(self.labelProductosComprar)

        # Layout para la opción de compra y generación de factura
        boxComprar = QHBoxLayout()
        facturaCheck = QCheckBox("Factura")
        btnComprar = QPushButton("Comprar")
        btnComprar.pressed.connect(lambda: self.on_comprar_pressed(facturaCheck.isChecked()))
        boxComprar.addWidget(facturaCheck)
        boxComprar.addWidget(btnComprar)
        box.addLayout(boxComprar)

        # Botón para ver las compras realizadas
        btnCompras = QPushButton("Ver Compras")
        btnCompras.pressed.connect(lambda: self.changeToSeeBoughts())
        box.addWidget(btnCompras)

        container = QWidget()
        container.setLayout(box)
        return container

    def seeBoughtsView(self):
        """
        Configura la vista de las compras realizadas por el usuario.
        """
        box = QVBoxLayout()
        compras = self.controller.consultar_compra(self.cliente.username)
        print(compras)

        # Crear tabla para mostrar las compras
        tabla = QTableView()
        modeloTabla = ModeloTaboa(compras, ["ID compra", "Nombre", "Compra", "Total"])
        tabla.setModel(modeloTabla)
        tabla.resizeColumnsToContents()

        # Configurar selección de filas en la tabla
        tabla.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        tabla.setSelectionMode(QTableView.SelectionMode.SingleSelection)
        tabla.selectRow(0)

        # Crear el botón para volver a la vista de productos
        botonVolver = QPushButton("Ir a comprar")
        botonVolver.pressed.connect(lambda: self.changeToLoggedView("Compras"))

        # Añadir tabla y botón al layout
        box.addWidget(tabla)
        box.addWidget(botonVolver)

        if self.admin:
            botonBorrar = QPushButton("Borrar Compra")
            botonBorrar.pressed.connect(lambda: self.borrar_compra(compras[seleccion.selectedIndexes()[0].row()][0]))
            box.addWidget(botonBorrar)

        container = QWidget()
        container.setLayout(box)
        return container

    def borrar_compra(self, id_compra):
        """
        Borra una compra y actualiza la vista de compras.

        :param id_compra: ID de la compra a borrar
        """
        self.controller.borrar_compra(id_compra)
        self.ventanaCompras.hide()
        self.ventanaCompras = self.seeBoughtsView()
        self.ventanaCompras.show()
        self.contenedorPrincipal.addWidget(self.ventanaCompras)

    def addItemsToComboProductos(self):
        """
        Añade productos al combo box de productos disponibles.
        """
        self.comboProductos.clear()
        productos = self.controller.consultar_producto_servicio()
        for producto in productos:
            print(producto)
            texto = producto[0] + ", " + str(producto[2]) + "€"
            self.comboProductos.addItem(texto)

    def on_comprar_pressed(self, facturaCheck):
        """
        Procesa la compra de los productos seleccionados

        :param facturaCheck: booleano que indica si se desea generar una factura
        """
        print(self.cliente.username + " va a comprar: " + str(self.productbuy) + " por un total de: " + str(
            self.total) + "€")
        if facturaCheck:
            id = self.controller.insertar_compra(self.cliente.username, self.productbuy, self.total)
            print(id)
            Informe(id=id, username=self.cliente.username, compras=self.productbuy, total=self.total,
                    nombre=self.cliente.nombre, apellido=self.cliente.apellido, direccion=self.cliente.direccion,
                    telefono=self.cliente.telefono)
            print("Factura generada")

        # Reiniciar la lista de productos en la cesta y el total
        self.labelProductosComprar.setText("Productos en la cesta: ")
        self.productbuy = []
        self.total = 0

    def addProduct(self, item, cantidad):
        """
        Añade un producto a la cesta de compras.

        :param cantidad: cantidad del producto
        :param item: producto que desea adicionar
        """
        # Separar el nombre y el precio del producto
        item = item.split(",")
        self.productbuy.append((item[0], item[1], cantidad))
        print(float(item[1].split("€")[0].lstrip()))
        print(self.productbuy)

        # Calcular el total de la compra
        self.total = self.total + int(cantidad) * float(item[1].split("€")[0].lstrip())
        print(self.total)

        # Reiniciar el combo box y el campo de cantidad
        self.comboProductos.setCurrentIndex(0)
        self.cantidad.clear()

        # Actualizar la etiqueta de productos en la cesta
        self.labelProductosComprar.setText(
            self.labelProductosComprar.text() + "\n " + item[0] + ", " + str(cantidad) + " unidades, " + str(
                item[1]) + " = " + str(int(cantidad) * float(item[1].split("€")[0])) + "€")

    def createProduct(self, nombre, descripcion, precio):
        """
        Crea un nuevo producto.

        :param nombre: Nombre del producto
        :param descripcion: Descripcion del producto
        :param precio: Precio del producto
        """
        print("Crear Producto")
        self.controller.insertar_producto_servicio(nombre, descripcion, precio)
        self.comboProductos.addItem(nombre + ", " + str(precio) + "€")

    def editProduct(self, nombre, descripcion, precio):
        """
        Edita un producto existente.

       :param nombre: Nombre del producto
       :param descripcion: Descripcion del producto
       :param precio
        """
        self.controller.modificar_producto_servicio(nombre, descripcion, precio)
        self.addItemsToComboProductos()

    def deleteProduct(self, nombre):
        """
        Borra un producto existente.

        :param nombre: Nombre del producto
        """
        self.controller.borrar_producto_servicio(nombre)
        self.addItemsToComboProductos()

    def on_loggin_pressed(self, text, username, password, nombre, apellido, direccion, telefono, admin):
        """
        Maneja la acción de iniciar sesión o registrarse.

        :param text: texto del usuario
        :param username: username
        :param password: password
        :param nombre: nombre del usuario
        :param apellido: apellido del usuario
        :param direccion: direccion del usuario
        :param telefono: telefono del usuario
        :param admin: admin del usuario
        """
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
        """
        Cambia a la vista de usuario logueado.

        :param proveniente:
        """
        self.total = 0
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

    def changeToSeeBoughts(self):
        """
        Cambia a la vista de las compras realizadas.
        """
        self.ventanaLogged.hide()
        print("Cambiando a la vista de compras")
        self.ventanaCompras = self.seeBoughtsView()
        self.ventanaCompras.show()
        self.contenedorPrincipal.addWidget(self.ventanaCompras)

    def on_register_pressed(self):
        """
        Maneja la acción de cambiar entre registro e inicio de sesión.
        """
        if self.bRegister.text() == "Registrarse":
            self.bRegister.setText("Inicio de Sesión")
            self.bLogin.setText("Crear Usuario")
            self.hide_show_register()
        else:
            self.bRegister.setText("Registrarse")
            self.bLogin.setText("Iniciar Sesión")
            self.hide_show_register()

    def hide_show_register(self):
        """
        Muestra u oculta los campos de registro dependiendo del estado del botón.
        """
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
