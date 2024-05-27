from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, Spacer

class Informe:
    def __init__(self, id = "", username = "", compras = "", total = "", nombre= "", apellido="",telefono = "", direccion = ""):
        self.hojaEstilo = getSampleStyleSheet()
        self.elementosDoc = []
        print("Informe: ", id, username, compras, total)
        self.cabecera()
        self.tablaFactura(nombre, apellido, telefono, direccion, id)
        self.tablaDescripcionCompra(id, username, compras, total)
        documento = SimpleDocTemplate(f"facturaClimatizacion_{id}.pdf", pagesize=A4)
        try:
            documento.build(self.elementosDoc)
            print("El documento se ha creado correctamente")
        except Exception as e:
            print("Ocurrió un error al crear el documento: ", e)

    def tablaDescripcionCompra(self, id, username, compras, total):
        textoCompra = ""
        for producto in compras:
            textoCompra += producto[0] + ", " + producto[1] + " x " + str(producto[2]) + "; "
        totalTexto = str(total) + " €"
        elementos = [
            ["ID Factura", "Username", "Compra", "Total"],
            [id, username, textoCompra, totalTexto]
        ]
        estilo = [
            ("GRID", (0, 0), (-1, -1), 1, "black"),
            ("ALIGN", (0, 0), (-1, 0), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ]
        tabla = Table(data=elementos, style=estilo, colWidths=[55, 100, 200, 100])
        self.elementosDoc.append(tabla)


    def tablaFactura(self, nombre, apellido, telefono, direccion, id):
        fecha_actual = datetime.now().date()
        fecha = fecha_actual.strftime("%d/%m/%Y")
        elementos_izquierda = [
            ["Nombre", nombre],
            ["Apellido", apellido],
            ["Teléfono", telefono],
            ["Dirección de facturación", direccion],
            ["Fecha", fecha]
        ]
        estilo_izquierda = [
            ("LEFTPADDING", (0, 0), (-1, -1), 0)
        ]
        tabla_izquierda = Table(data=elementos_izquierda, style=estilo_izquierda, colWidths=120, rowHeights=15)

        elementos_derecha = [
            ["Nombre", "Climatización"],
            ["Teléfono", "986 123 456"],
            ["Dirección", "A Madroa, 21"],
        ]

        estilo_derecha = [
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),  # le quitamos el padding
        ]
        tabla_derecha = Table(data=elementos_derecha, style=estilo_derecha, colWidths=100, rowHeights=25)

        elementos_tabla = [
            ["FACTURAR A:", "DATOS FACTURA"],
            [tabla_izquierda, tabla_derecha]
        ]

        estilo_tabla = [
            ("FONTSIZE", (-1, 0), (-1, 0), 14),
            ("BACKGROUND", (0, 0), (-1, -1), "whitesmoke")
        ]

        tabla = Table(data=elementos_tabla, style=estilo_tabla, colWidths=230)
        self.elementosDoc.append(tabla)
        self.elementosDoc.append(Spacer(0, 25))
        print("Tabla añadida")

    def cabecera(self):

        estilo_procedente = [
            ("FONTSIZE", (0,0), (-1,-1), 12),
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold")
        ]

        datos_tabla_procedente = [
            ["Nombre", "Climatización"],
            ["Teléfono", "986 123 456"],
            ["Dirección", "A Madroa, 21"]
        ]

        tabla_procedente  = Table(data=datos_tabla_procedente, style=estilo_procedente, colWidths=[100, 100, 100])

        estilo = [
            ("VALIGN", (0, 0), (0, -1), "MIDDLE"),
            ("ALIGN", (0, 0), (0, -1), "CENTER"),
            ("ALIGN", (0, -1), (0, -1), "RIGHT"),
            ("GRID", (0, 0), (-1, -1), 1, "black"),
            ("INNERGRID", (0, 0), (-1, -1), 1, "black"),
        ]

        cabecera_estilo = self.hojaEstilo["Heading1"]
        cabecera_estilo.fontSize = 14
        cabecera = Paragraph("FACTURA CLIMATIZACION", cabecera_estilo)

        elementos_cabecera = [
            [cabecera],
            [tabla_procedente]
        ]

        tabla = Table(data=[[elementos_cabecera]], style=estilo, colWidths=460)
        self.elementosDoc.append(tabla)
        print("Cabecera añadida")
        self.elementosDoc.append(Spacer(0, 20))
        print("Espacio añadido")