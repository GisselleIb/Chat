import unittest
import sys
sys.path.append('../..')
from src.cliente import Cliente
class ClienteTest(unittest.TestCase):
    client=Cliente(socket.gethostname(),80)
    def test_cliente(self):
        pass

    def test_seConecto(self):
        self.assertTrue(client.seConecto())
    def test_desconectado(self):
        self.assertTrue(client.desconectado)

    def test_enviado(self):
        pass

    def test_respuesta(self):
        pass
if __name__ == '__main__':
    unittest.main()
