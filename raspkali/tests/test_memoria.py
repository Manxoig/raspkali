import unittest
from widget import memoria

class TestMemoria(unittest.TestCase):
    def test_memoria_ram(self):
        result = memoria.memoria_ram()
        self.assertIsInstance(result, str)
        self.assertIn('%', result)
        self.assertIn('MB', result)

    def test_almacenamiento(self):
        result = memoria.almacenamiento()
        self.assertIsInstance(result, str)
        self.assertIn('%', result)
        self.assertIn('GB', result)

if __name__ == '__main__':
    unittest.main()