# Clase Cliente
class Cliente:
    def __init__(self, username, contraseña, nombre, apellido, telefono, direccion, admin):
        # username clave primaria
        self.username = username
        self.contraseña = contraseña
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.direccion = direccion
        self.admin = admin



    def __str__(self):
        return f"UserName: {self.username}, Nombre: {self.nombre}, Apellido: {self.apellido}, Telefono: {self.telefono}, Direccion: {self.direccion}, Admin: {self.admin}"