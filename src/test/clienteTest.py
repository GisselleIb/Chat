import unittest
import sys
sys.path.append('../..')
from src.cliente import Cliente
class ClienteTest(unittest.TestCase):

    def test_cliente(self):
        pass

    def test_seConecto(self):
        client=Cliente(socket.gethostname(),65)
        self.assertFalse(client.seConecto())
        client.setPort(80)
        self.assertTrue(client.seConecto())
    def test_desconectado(self):
        self.assertEqual("Desconectando del servidor",client.desconectado())

    def test_enviado(self):
        client=Cliente(socket.gethostname(),80)
        assertFalse(client.seConecto())

    def test_respuesta(self):
        pass
if __name__ == '__main__':
    unittest.main()
