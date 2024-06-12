import conexionBD
from Cliente import Cliente
from ProductoServicio import ProductoServicio


class Controller:
    def __init__(self):
        # Inicializamos la conexión a la base de datos
        self.conexion = conexionBD.ConexionBD("climatizacion.db")
        self.conexion.conectaBD()
        self.conexion.creaCursor()

    def insertar_compra(self, username, compra, total):
        """
        Inserta una nueva compra en la base de datos.
        """
        # Construimos la descripción de la compra
        textoCompra = ""
        for producto in compra:
            textoCompra += producto[0] + producto[1] + " x " + str(producto[2]) + "; "
            print(textoCompra)

        # Insertamos la compra en la base de datos y devolvemos el ID de la inserción
        inserccion = self.conexion.engadeRexistroDevolveId(
            "INSERT INTO compra (username, compra, total) VALUES (?, ?, ?)",
            username, textoCompra, total
        )
        print(inserccion)
        return inserccion

    def consultar_compra(self, username):
        """
        Consulta las compras de un usuario específico.
        """
        compra = self.conexion.consultaConParametros("SELECT * FROM compra WHERE username = ?", username)
        return compra

    def borrar_compra(self, id):
        """
        Borra una compra específica de la base de datos.
        """
        self.conexion.borraRexistro("DELETE FROM compra WHERE id = ?", id)

    # ProductoServicio
    def insertar_producto_servicio(self, nombre, descripcion, precio):
        """
        Inserta un nuevo producto o servicio en la base de datos.

        :param nombre: Nombre del producto
        :param descripcion: Descripcion del producto
        :param precio: Precio del producto
        """
        inserccion = self.conexion.engadeRexistro(
            "INSERT INTO producto_servicio VALUES (?, ?, ?)",
            nombre, descripcion, precio
        )
        if inserccion:
            print("Producto/Servicio insertado")

    def modificar_producto_servicio(self, nombre, descripcion, precio):
        """
        Modifica un producto o servicio existente en la base de datos.

        :param nombre: Nombre del producto
        :param descripcion: Descripcion del producto
        :param precio: Precio del producto

        """
        modificacion = self.conexion.actualizaRexistro(
            "UPDATE producto_servicio SET descripcion = ?, precio = ? WHERE nombre = ?", descripcion, precio, nombre)
        if modificacion:
            print("Producto/Servicio modificado")

    def consultar_producto_servicio(self):
        """
        Consulta todos los productos y servicios en la base de datos.
        """
        producto_servicio = self.conexion.consultaSenParametros("SELECT * FROM producto_servicio")
        for producto in producto_servicio:
            productos = ProductoServicio(producto[0], producto[1], producto[2])
            print(productos.__str__())
        return producto_servicio

    def borrar_producto_servicio(self, nombre):
        """
        Borra un producto o servicio específico de la base de datos.

        :param nombre: Nombre del producto
        """
        borrado = self.conexion.actualizaRexistro("DELETE FROM producto_servicio WHERE nombre = ?", nombre)
        if borrado:
            print("Producto/Servicio borrado")

    # Clientes
    def insertar_cliente(self, username, contraseña, nombre, apellido, direccion, telefono, admin):
        """
        Inserta un nuevo cliente en la base de datos.

        :param username: Nombre del cliente
        :param contraseña:
        :param nombre:
        :param apellido:
        :param direccion:
        :param telefono:
        :param admin
        """
        cliente = Cliente(username=username, contraseña=contraseña, nombre=nombre, apellido=apellido,
                          direccion=direccion, telefono=telefono, admin=admin)
        print(cliente.__str__())
        return self.conexion.engadeRexistro(
            "INSERT INTO cliente VALUES (?, ?, ?, ?, ?, ?, ?)",
            username, contraseña, nombre, apellido, direccion, telefono, admin
        )

    def consultar_cliente(self, username, contraseña):
        """
        Consulta si las credenciales de un cliente son correctas.

        :param username: Nombre del cliente
        :param contraseña: Contraseña del cliente
        """
        cliente = self.conexion.consultaConParametros("SELECT contraseña FROM cliente WHERE username = ?", username)
        if cliente[0][0] == contraseña:
            return True
        else:
            return False

    def get_cliente(self, username):
        """
        Obtiene los datos de un cliente específico.

        :param username: Nombre del cliente
        """
        cliente = self.conexion.consultaConParametros("SELECT * FROM cliente WHERE username = ?", username)
        return Cliente(cliente[0][0], cliente[0][1], cliente[0][2], cliente[0][3], cliente[0][4], cliente[0][5],
                       cliente[0][6])

    def modificar_cliente(self, username):
        """
        Modifica los datos de un cliente específico.

        :param username: Nombre del cliente
        """
        modificacion = self.conexion.actualizaRexistro("UPDATE cliente SET nombre = ? WHERE username = ?", "Javier",
                                                       username)
        if modificacion:
            print("Cliente modificado")