import socket
class Sala():

    def __init__(self,nombre,dueño):
        self.nombre=nombre
        self.dueño=dueño
        self.clientes=[]
        self.invitados=[]
        self.clientes.append(dueño)

    def agregaInv(self,invitado):
        self.invitados.append(invitado)

    def agrega(self,cliente):
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
        self.clientes.remove(cliente)
