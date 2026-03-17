import unittest
from unittest.mock import patch
from widget import temperatura

class TestTemperatura(unittest.TestCase):
    @patch('subprocess.check_output')
    def test_temperatura_cpu_found(self, mock_check):
        mock_check.return_value = b'coretemp-isa-0000\nAdapter: ISA adapter\ntemp1: +45.0°C (crit = +100.0°C)\n'
        result = temperatura.temperatura_cpu()
        self.assertEqual(result, '+45.0°C')

    @patch('subprocess.check_output')
    def test_temperatura_cpu_not_found(self, mock_check):
        mock_check.return_value = b'coretemp-isa-0000\nAdapter: ISA adapter\n'
        result = temperatura.temperatura_cpu()
        self.assertEqual(result, 'No detectada')

    @patch('subprocess.check_output', side_effect=Exception)
    def test_temperatura_cpu_error(self, mock_check):
        result = temperatura.temperatura_cpu()
        self.assertEqual(result, 'No disponible')

if __name__ == '__main__':
    unittest.main()