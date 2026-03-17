import unittest
from unittest.mock import patch
from widget import servicios

class TestServicios(unittest.TestCase):
    @patch('widget.servicios.subprocess.check_output')
    def test_estado_servicio_active(self, mock_check):
        mock_check.return_value = b'active\n'
        result = servicios.estado_servicio('ssh')
        self.assertEqual(result, 'ssh: active')
        mock_check.assert_called_once_with(['systemctl', 'is-active', 'ssh'])

    @patch('widget.servicios.subprocess.check_output')
    def test_estado_servicio_inactive(self, mock_check):
        mock_check.return_value = b'inactive\n'
        result = servicios.estado_servicio('apache2')
        self.assertEqual(result, 'apache2: inactive')
        mock_check.assert_called_once_with(['systemctl', 'is-active', 'apache2'])

    @patch('widget.servicios.subprocess.check_output', side_effect=Exception)
    def test_estado_servicio_error(self, mock_check):
        result = servicios.estado_servicio('mysql')
        self.assertEqual(result, 'mysql: No disponible')
        mock_check.assert_called_once_with(['systemctl', 'is-active', 'mysql'])

if __name__ == '__main__':
    unittest.main()