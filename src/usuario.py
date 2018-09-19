class Usuario():
    """Clase Usuario que guarda el nombre del usuario
        y sus contactos
    """
    def __init__(self, nombre):
        self.nombre = nombre
        self.estado="ACTIVE"

    def asignaEstado(self,estado):
        self.estado=estado

    def getNombre(self):
        return self.nombre

    def setNombre(self,nombre):
        self.nombre=nombre
