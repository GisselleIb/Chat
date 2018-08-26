import sys
import unittest
import socket
sys.path.append('../..')
from src.servidor import Servidor
class ServidorTest(unittest.TestCase):

    def test_conectaCliente(self):
        serv=Servidor('',68)
        with self.assertRaises(socket.error):
            serv.conectaCliente()
        serv.setHost('')
        serv.setPort(80)
        assertTrue(serv.conectaCliente())

    def test_muerto(self):
        serv=Servidor('',80)
        self.assertTrue(serv.muerto())

    def test_escucha(self):
        serv=Servidor('',80)
        self.assertEqual(serv.escucha(),"Servidor escuchando")

    def test_acepta(self):
        pass

    def test_enviaRespuesta(self):
        pass

    def test_lee(self):
        pass

    def test_getHost(self):
        serv=Servidor('',80)
        self.assertEqual(serv.getHost(),'')

    def test_getPort(self):
        serv=Servidor('',80)
        self.assertEqual(serv.getPort(),80)

    def test_setHost(self):
        serv=Servidor('',80)
        self.assertEqual(serv.getHost(),'')
        serv.setHost(socket.gethostname())
        self.assertEqual(socket.gethostname(),serv.getHost())

    def test_setPort(self):
        serv=Servidor('',80)
        self.assertEqual(serv.getPort(),80)
        serv.setPort(8888)
        self.assertEqual(serv.getPort(),8888)


if __name__ == '__main__':
    unittest.main()
