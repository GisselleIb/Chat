import socket
class Sala():
    """Clase Sala a la cual se le asigna un dueño y un nombre,
    agrega clientes invitados y a los clientes que han aceptado
    unirse.
    """

    def __init__(self,nombre,dueño):
        """Constructor de la clase
        Parámetros
        ----------
        nombre : str
            Nombre de la sala
        dueño : socket
            Conexión del dueño de la sala
        clientes : [socket]
            Lista de sockets de los miembros de la sala
        invitados : [socket]
            Lista de sockets de gente invitada pero que no se ha
            unido a la sala
        """
        self.nombre=nombre
        self.dueño=dueño
        self.clientes=[]
        self.invitados=[]
        self.clientes.append(dueño)

    def agregaInv(self,invitado):
        """Agrega un socket a la lista de invitados
        Parámetros
        ----------
        invitado : socket
            Socket del usuario invitado a la sala
        """
        self.invitados.append(invitado)

    def agrega(self,cliente):
        """Agrega un socket a la lista de clientes
        Parámetros
        ----------
        cliente : socket
            Socket del cliente que se unió a la sala
        """
        if cliente in self.clientes:
            cliente.sendall("Ya perteneces a la sala".encode())
            return
        if cliente in self.invitados:
            self.clientes.append(cliente)
            print("se unio a la sala")
            msg="Te has unido a: "+self.nombre
            cliente.sendall(msg.encode())
            self.invitados.remove(cliente)
        else:
            cliente.sendall("No estas invitado a la sala".encode())

    def elimina(self,cliente):
        """Elimina un cliente de la lista de la lista de clientes
        Parámetros
        ----------
        cliente : socket
            Socket del cliente a eliminar
        """
        self.clientes.remove(cliente)
