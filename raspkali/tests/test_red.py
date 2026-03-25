import unittest
from unittest.mock import patch, MagicMock
from raspkali_widget import red


class TestRed(unittest.TestCase):

    @patch('raspkali_widget.red.requests.get')
    def test_obtener_ip_publica_exito(self, mock_get):
        mock_get.return_value.text = '192.168.1.1'
        result = red.obtener_ip_publica()
        self.assertEqual(result, '192.168.1.1')
        mock_get.assert_called_once_with('https://ifconfig.me', timeout=5)

    @patch('raspkali_widget.red.requests.get', side_effect=Exception)
    def test_obtener_ip_publica_error(self, mock_get):
        result = red.obtener_ip_publica()
        self.assertEqual(result, 'No disponible')

    def test_listar_interfaces_retorna_lista(self):
        result = red.listar_interfaces()
        self.assertIsInstance(result, list)
        for item in result:
            self.assertIsInstance(item, str)

    def test_velocidad_por_interfaz_retorna_dict(self):
        result = red.velocidad_por_interfaz()
        self.assertIsInstance(result, dict)

    def test_velocidad_por_interfaz_estructura(self):
        # Primera llamada inicializa el estado
        red._prev_counters = {}
        red._prev_time = None
        result = red.velocidad_por_interfaz()
        for key, value in result.items():
            self.assertIsInstance(key, str)
            self.assertIsInstance(value, dict)
            self.assertIn('enviados', value)
            self.assertIn('recibidos', value)

    def test_velocidad_por_interfaz_segunda_llamada_retorna_strings(self):
        # Segunda llamada debe retornar valores formateados como strings
        red._prev_counters = {}
        red._prev_time = None
        red.velocidad_por_interfaz()   # inicializa
        import time
        time.sleep(0.1)
        result = red.velocidad_por_interfaz()
        for value in result.values():
            self.assertIsInstance(value['enviados'], str)
            self.assertIsInstance(value['recibidos'], str)


if __name__ == '__main__':
    unittest.main()
