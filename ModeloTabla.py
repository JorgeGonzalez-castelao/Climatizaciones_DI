from PyQt6.QtCore import Qt, QAbstractTableModel
from PyQt6.QtGui import QColor


class ModeloTaboa(QAbstractTableModel):
    """
    Clase que hereda de QAbstractTableModel para crear un modelo de tabla
    A partir de esta clase se creará un modelo de tabla que se usará para cambiar el estilo de la tabla
    """
    def __init__(self, table, headerData):
        super().__init__()
        self.table = table
        self.headerData = headerData

    def rowCount(self, index):
        return len(self.table)

    def columnCount(self, index):
        return len(self.table[0])

    # to fill the table
    def data(self, index, role):
        if index.isValid():
            if role == Qt.ItemDataRole.EditRole or role == Qt.ItemDataRole.DisplayRole:
                return self.table[index.row()][index.column()]
            ''' color texto
            if role == Qt.ItemDataRole.ForegroundRole:
                if self.table[index.row()][3]:
                    return QColor(255,0,0)
            '''
            # color de fondo
            '''
            if role == Qt.ItemDataRole.BackgroundRole:
                if self.table[index.row()][0] == "nico":
                    return QColor(255,80,150)
                else:
                    return QColor(0,150,255)
            '''

    # to edit the table
    def setData(self, index, value, role):
        if role == Qt.ItemDataRole.EditRole:
            self.table[index.row()][index.column()] = value
            return True
        return False

     # esta funcion es para que se pueda editar la tabla (por defecto no se puede)
    def flags(self, index):
        return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsSelectable

    def headerData(self, section, orientation, role):
        # para añadir la cabezera
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self.headerData[section]
            ''' para que se ponga a la izquierda numeros
            elif orientation == Qt.Orientation.Vertical:
                return section + 1
            '''