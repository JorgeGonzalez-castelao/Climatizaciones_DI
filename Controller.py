import conexionBD
from Cliente import Cliente
from ProductoServicio import ProductoServicio


class Controller:
    def __init__(self):
        self.conexion = conexionBD.ConexionBD("climatizacion.db")
        self.conexion.conectaBD()
        self.conexion.creaCursor()

    # ProductoServicio
    def insertar_producto_servicio(self, nombre, descripcion, precio):
        inserccion = self.conexion.engadeRexistro(
            "INSERT INTO producto_servicio VALUES (?, ?, ?)",
            nombre, descripcion, precio
        )
        if inserccion:
            print("Producto/Servicio insertado")

    def consultar_producto_servicio(self, nombre):
        producto_servicio = self.conexion.consultaConParametros("SELECT * FROM producto_servicio WHERE nombre = ?", nombre)
        for producto in producto_servicio:
            productos = ProductoServicio(producto[0], producto[1], producto[2])
            print(productos.__str__())
        return producto_servicio

    def borrar_producto_servicio(self, nombre):
        borrado = self.conexion.actualizaRexistro("DELETE FROM producto_servicio WHERE nombre = ?", nombre)
        if borrado:
            print("Producto/Servicio borrado")

    # Clientes
    def insertar_cliente(self, username, contraseña, nombre, apellido, telefono, direccion, admin):
        cliente = Cliente(username, contraseña, nombre, apellido, telefono, direccion, admin)
        print(cliente.__str__())
        return self.conexion.engadeRexistro(
            "INSERT INTO cliente VALUES (?, ?, ?, ?, ?, ?, ?)",
            username, contraseña, nombre, apellido, telefono, direccion, admin
        )

    def consultar_cliente(self, username, contraseña):
        cliente = self.conexion.consultaConParametros("SELECT contraseña FROM cliente WHERE username = ?", username)
        if cliente[0][0] == contraseña:
            return True
        else:
            return False

    def modificar_cliente(self, username):
        modificacion = self.conexion.actualizaRexistro("UPDATE cliente SET nombre = ? WHERE username = ?", "Javier", username)
        if modificacion:
            print("Cliente modificado")