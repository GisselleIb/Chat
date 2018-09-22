class Usuario():
    """Clase Usuario que guarda el nombre del usuario
        y sus contactos
    """
    def __init__(self, nombre):
        """Constructor de la Clase
        Parámetros
        ----------
        nombre= str
            Nombre del usuario
        """
        self.nombre = nombre
        self.estado="ACTIVE"

    def asignaEstado(self,estado):
        """Actualiza el estado del usuario
        Parámetros
        ----------
        estado : str
            Estado nuevo del usuario
        """
        self.estado=estado

    def getNombre(self):
        """Getter del Usuario
        """
        return self.nombre

    def setNombre(self,nombre):
        """Setter del Usuario
        """
        self.nombre=nombre
