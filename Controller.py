import conexionBD
from Cliente import Cliente
from ProductoServicio import ProductoServicio


class Controller:
    def __init__(self):
        self.conexion = conexionBD.ConexionBD("climatizacion.db")
        self.conexion.conectaBD()
        self.conexion.creaCursor()

    def insertar_compra(self, username, compra, total):
        textoCompra = ""
        for producto in compra:
            textoCompra += producto[0] + producto[1] + " x " + str(producto[2]) + "; "
            print(textoCompra)
        inserccion = self.conexion.engadeRexistroDevolveId(
            "INSERT INTO compra (username, compra, total) VALUES (?, ?, ?)",
            username, textoCompra, total
        )
        print(inserccion)
        return inserccion

    def consultar_compra(self, username):
        compra = self.conexion.consultaConParametros("SELECT * FROM compra WHERE username = ?", username)
        return compra

    def borrar_compra(self, id):
        self.conexion.borraRexistro("DELETE FROM compra WHERE id = ?", id)


    # ProductoServicio
    def insertar_producto_servicio(self, nombre, descripcion, precio):
        inserccion = self.conexion.engadeRexistro(
            "INSERT INTO producto_servicio VALUES (?, ?, ?)",
            nombre, descripcion, precio
        )
        if inserccion:
            print("Producto/Servicio insertado")

    def modificar_producto_servicio(self, nombre, descripcion, precio):
        modificacion = self.conexion.actualizaRexistro("UPDATE producto_servicio SET descripcion = ?, precio = ? WHERE nombre = ?", descripcion, precio, nombre)
        if modificacion:
            print("Producto/Servicio modificado")

    def consultar_producto_servicio(self):
        producto_servicio = self.conexion.consultaSenParametros("SELECT * FROM producto_servicio")
        for producto in producto_servicio:
            productos = ProductoServicio(producto[0], producto[1], producto[2])
            print(productos.__str__())
        return producto_servicio

    def borrar_producto_servicio(self, nombre):
        borrado = self.conexion.actualizaRexistro("DELETE FROM producto_servicio WHERE nombre = ?", nombre)
        if borrado:
            print("Producto/Servicio borrado")

    # Clientes
    def insertar_cliente(self, username, contraseña, nombre, apellido, direccion, telefono, admin):
        cliente = Cliente(username=username, contraseña=contraseña, nombre=nombre, apellido=apellido, direccion=direccion, telefono=telefono, admin=admin)
        print(cliente.__str__())
        return self.conexion.engadeRexistro(
            "INSERT INTO cliente VALUES (?, ?, ?, ?, ?, ?, ?)",
            username, contraseña, nombre, apellido, direccion, telefono, admin
        )

    def consultar_cliente(self, username, contraseña):
        cliente = self.conexion.consultaConParametros("SELECT contraseña FROM cliente WHERE username = ?", username)
        if cliente[0][0] == contraseña:
            return True
        else:
            return False

    def get_cliente(self, username):
        cliente = self.conexion.consultaConParametros("SELECT * FROM cliente WHERE username = ?", username)
        return Cliente(cliente[0][0], cliente[0][1], cliente[0][2], cliente[0][3], cliente[0][4], cliente[0][5], cliente[0][6])

    def modificar_cliente(self, username):
        modificacion = self.conexion.actualizaRexistro("UPDATE cliente SET nombre = ? WHERE username = ?", "Javier", username)
        if modificacion:
            print("Cliente modificado")