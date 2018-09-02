import unittest
sys.path.append('../..')
from src.usuario import Usuario
class UsuarioTest(unittest.TestCase):
    usuario=Usuario("name")
    def test_getNombre(self):
        self.assertEqual(self.usuario.getNombre(),"name")

    def test_setNombre(self):
        self.assertEqual(self.usuario.getNombre(),"name")
        self.usuario.setNombre("nombre")
        self.assertEqual(self.usuario.getNombre(),"name")
        self.usuario.setNombre("name")

    def test_agregaContacto(self):


    def test_eliminaContacto(self):
