import unittest
from widget import puertos

class TestPuertos(unittest.TestCase):
    def test_puertos_abiertos(self):
        result = puertos.puertos_abiertos()
        self.assertIsInstance(result, list)
        for item in result:
            self.assertIsInstance(item, str)
        # Al menos debería haber algo, pero en test puede ser vacío

if __name__ == '__main__':
    unittest.main()