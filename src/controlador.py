
class Controlador():
    """Clase controlador que interactua con el cliente y la interfaz."""
    def __init__(self,cliente):
        """Constructor de la clase
        Parámetros
        ----------
        cliente : Cliente
            Objeto cliente con el que el controlador se comunicara
        """
        self.cliente=cliente

    def actualizaCliente(self,evento):
        """Método que pasa los datos recibidos desde la interfaz
        y los pasa al cliente para ser procesados
        Parámetros
        ----------
        evento : str
            Evento a ser procesado por el cliente
        """
        self.cliente.comandos(evento)
