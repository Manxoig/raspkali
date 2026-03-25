import unittest
from unittest.mock import patch, MagicMock
from raspkali_widget import puertos


class TestPuertos(unittest.TestCase):

    def test_puertos_abiertos_retorna_lista(self):
        result = puertos.puertos_abiertos()
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

    def test_puertos_abiertos_elementos_string(self):
        result = puertos.puertos_abiertos()
        for item in result:
            self.assertIsInstance(item, str)

    @patch('raspkali_widget.puertos.psutil.net_connections')
    def test_puertos_sin_conexiones_retorna_ninguno(self, mock_conn):
        mock_conn.return_value = []
        result = puertos.puertos_abiertos()
        self.assertEqual(result, ["Ninguno"])

    @patch('raspkali_widget.puertos.psutil.net_connections')
    def test_puertos_filtra_solo_listen(self, mock_conn):
        c1 = MagicMock()
        c1.status = 'LISTEN'
        c1.laddr.port = 22
        c1.type = 'SOCK_STREAM'

        c2 = MagicMock()
        c2.status = 'ESTABLISHED'
        c2.laddr.port = 443
        c2.type = 'SOCK_STREAM'

        mock_conn.return_value = [c1, c2]
        result = puertos.puertos_abiertos()
        self.assertEqual(len(result), 1)
        self.assertIn('22', result[0])


if __name__ == '__main__':
    unittest.main()
