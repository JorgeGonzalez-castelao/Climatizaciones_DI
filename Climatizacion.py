from Controller import Controller

class Climatizacion:
    def __init__(self):
        # interfaz grafica
        self.controller = Controller()
        if self.controller.insertar_cliente("Pepe", "Perez", 666666666, "Calle Falsa 123"):
            print("Cliente insertado")
        print(self.controller.consultar_cliente(666666666))
        self.controller.modificar_cliente(666666666)
        print(self.controller.consultar_cliente(666666666))

if __name__ == "__main__":
    print("Inicio")
    climatizacion = Climatizacion()
    print("Fin")