from guiChat import GUIChat
from cliente import Cliente
from PyQt5 import QtWidgets
import threading
import sys
class Controlador():
    """docstring fo Controlador."""
    def __init__(self,cliente):
        self.cliente=cliente

    def actualizaCliente(self,evento):
        self.cliente.comandos(evento)
