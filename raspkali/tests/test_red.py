import unittest
from unittest.mock import patch
from widget import red

class TestRed(unittest.TestCase):
    @patch('requests.get')
    def test_obtener_ip_publica_success(self, mock_get):
        mock_get.return_value.text = '192.168.1.1'
        result = red.obtener_ip_publica()
        self.assertEqual(result, '192.168.1.1')

    @patch('requests.get', side_effect=Exception)
    def test_obtener_ip_publica_error(self, mock_get):
        result = red.obtener_ip_publica()
        self.assertEqual(result, 'No disponible')

    def test_listar_interfaces(self):
        result = red.listar_interfaces()
        self.assertIsInstance(result, list)
        for item in result:
            self.assertIsInstance(item, str)

    def test_velocidad_por_interfaz(self):
        result = red.velocidad_por_interfaz()
        self.assertIsInstance(result, dict)
        for key, value in result.items():
            self.assertIsInstance(key, str)
            self.assertIsInstance(value, dict)
            self.assertIn('enviados', value)
            self.assertIn('recibidos', value)
            self.assertIsInstance(value['enviados'], int)
            self.assertIsInstance(value['recibidos'], int)

if __name__ == '__main__':
    unittest.main()