import unittest
from unittest.mock import patch
from raspkali_widget import servicios


class TestServicios(unittest.TestCase):

    @patch('raspkali_widget.servicios.subprocess.check_output')
    def test_estado_servicio_activo(self, mock_check):
        mock_check.return_value = b'active\n'
        result = servicios.estado_servicio('ssh')
        self.assertEqual(result, 'ssh: active')
        mock_check.assert_called_once_with(['systemctl', 'is-active', 'ssh'], timeout=5)

    @patch('raspkali_widget.servicios.subprocess.check_output')
    def test_estado_servicio_inactivo(self, mock_check):
        mock_check.return_value = b'inactive\n'
        result = servicios.estado_servicio('apache2')
        self.assertEqual(result, 'apache2: inactive')
        mock_check.assert_called_once_with(['systemctl', 'is-active', 'apache2'], timeout=5)

    @patch('raspkali_widget.servicios.subprocess.check_output', side_effect=FileNotFoundError)
    def test_estado_servicio_no_disponible(self, mock_check):
        result = servicios.estado_servicio('mysql')
        self.assertEqual(result, 'mysql: No disponible')

    @patch('raspkali_widget.servicios.subprocess.check_output',
           side_effect=__import__('subprocess').TimeoutExpired(cmd='systemctl', timeout=5))
    def test_estado_servicio_timeout(self, mock_check):
        result = servicios.estado_servicio('nginx')
        self.assertEqual(result, 'nginx: No disponible')


if __name__ == '__main__':
    unittest.main()
