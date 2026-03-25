import unittest
from raspkali_widget import memoria


class TestMemoria(unittest.TestCase):

    def test_memoria_ram_formato(self):
        result = memoria.memoria_ram()
        self.assertIsInstance(result, str)
        self.assertIn('%', result)
        self.assertIn('MB', result)

    def test_almacenamiento_formato(self):
        result = memoria.almacenamiento()
        self.assertIsInstance(result, str)
        self.assertIn('%', result)
        self.assertIn('GB', result)


if __name__ == '__main__':
    unittest.main()
