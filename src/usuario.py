class Usuario():
    """Clase Usuario que guarda el nombre del usuario
        y sus contactos
    """
    def __init__(self, nombre):
        self.nombre = nombre
        self.directorio=[]

    def getNombre(self):
        return self.nombre

    def setNombre(self,nombre):
        self.nombre=nombre

    def agregaContacto(self,contacto):
        if(contacto != None):
            self.directorio.append(contacto)
        else:
            return "Inserte un contacto válido"

    def eliminaContacto(self,contacto):
        if(contacto in direccion):
            self.directorio.pop(contacto)
        else:
            return "No existe el contacto:" + contacto
