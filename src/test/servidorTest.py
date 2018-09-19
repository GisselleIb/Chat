import sys
import unittest
import socket
import _thread
sys.path.append('chat/src/test')
from src.servidor import Servidor
class ServidorTest(unittest.TestCase):
    serv=Servidor('',1234)
    def setUp(self):
        serv=Servidor('',1234)
        serv.conectaCliente()
        client= socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('', 1234))
        start_new_thread(serv.servidorVivo())

    def tearDown(self):
        client.close()

    def test_conectaCliente(self):
        self.assertFalse(serv.conectaCliente())
        serv.setHost('')
        serv.setPort(59243)
        self.assertTrue(serv.conectaCliente())

    def test_getHost(self):
        self.assertEqual(serv.getHost(),'')

    def test_getPort(self):
        self.assertEqual(serv.getPort(),1234)

    def test_setHost(self):
        self.assertEqual(serv.getHost(),'')
        serv.setHost(socket.gethostname())
        self.assertEqual(socket.gethostname(),serv.getHost())

    def test_setPort(self):
        self.assertEqual(serv.getPort(),1234)
        serv.setPort(8888)
        self.assertEqual(serv.getPort(),8888)

    def test_showUsuarios(self):
        serv.usuarios['a']=1
        serv.usuarios['b']=2
        client.send("USERS".encode())
        self.assertEqual(client.recv(4096).decode(),"a\nb")
    def test_identifica(self):
        client.send("IDENTIFY test".encode())
        self.assertEqual(client.recv(4096).decode(),"Identificación completada")
        self.assertTrue("test" in serv.usuarios)
    def test_invita(self):
        pass

    def test_creaSala(self):
        client.send("CREATROOM sala1")
        self.assertTrue("sala1" in serv.salas)

    def test_unirse(self):
        l=len(serv.salas["sala1"])
        client.send("JOINROOM sala1".encode())
        self.assertEqual(client.recv(4096).decode(),"Te has unido a: sala1")
        self.assertTrue(len(serv.salas["sala1"]) == l+1)
    def test_transmiteChat(self):
        pass

    def test_transmite(self):
        client.send("PUBLICMESSAGE msg".encode())
        self.assertEqual(client.recv(4096).decode(), "test: msg")

if __name__ == '__main__':
    unittest.main()
