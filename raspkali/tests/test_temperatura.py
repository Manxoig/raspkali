import unittest
from unittest.mock import patch
from raspkali_widget import temperatura


class TestTemperatura(unittest.TestCase):

    @patch('raspkali_widget.temperatura.subprocess.check_output')
    def test_temperatura_encontrada(self, mock_check):
        mock_check.return_value = (
            b'coretemp-isa-0000\nAdapter: ISA adapter\n'
            b'temp1:        +45.0\xc2\xb0C  (crit = +100.0\xc2\xb0C)\n'
        )
        result = temperatura.temperatura_cpu()
        self.assertEqual(result, '+45.0°C')
        mock_check.assert_called_once_with(['sensors'], timeout=5)

    @patch('raspkali_widget.temperatura.subprocess.check_output')
    def test_temperatura_no_detectada(self, mock_check):
        mock_check.return_value = b'coretemp-isa-0000\nAdapter: ISA adapter\n'
        result = temperatura.temperatura_cpu()
        self.assertEqual(result, 'No detectada')

    @patch('raspkali_widget.temperatura.subprocess.check_output',
           side_effect=FileNotFoundError)
    def test_temperatura_sensors_no_instalado(self, mock_check):
        result = temperatura.temperatura_cpu()
        self.assertEqual(result, 'No disponible')

    @patch('raspkali_widget.temperatura.subprocess.check_output',
           side_effect=__import__('subprocess').TimeoutExpired(cmd='sensors', timeout=5))
    def test_temperatura_timeout(self, mock_check):
        result = temperatura.temperatura_cpu()
        self.assertEqual(result, 'No disponible')


if __name__ == '__main__':
    unittest.main()
