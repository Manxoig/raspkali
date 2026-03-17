import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Agregar el path para importar ventana
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'debian/usr/local/bin'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'debian/usr/lib'))

from ventana import RaspKaliWidget

class TestVentanaLogic(unittest.TestCase):
    def setUp(self):
        # Mock QApplication to avoid GUI
        with patch('ventana.QApplication'):
            with patch('ventana.QWidget.__init__', return_value=None):
                with patch('ventana.QWidget.setWindowFlags'):
                    with patch('ventana.QWidget.setAttribute'):
                        with patch('ventana.QWidget.setGeometry'):
                            with patch('ventana.QWidget.setWindowOpacity'):
                                self.widget = RaspKaliWidget()
                                self.widget.label = MagicMock()
                                self.widget.timer_ip = MagicMock()
                                self.widget.timer_red = MagicMock()
                                self.widget.timer_proc = MagicMock()
                                self.widget.timer_sys = MagicMock()

    @patch('ventana.red.obtener_ip_publica', return_value='192.168.1.1')
    @patch('ventana.puertos.puertos_abiertos', return_value=['Puerto 22 (tcp)', 'Puerto 80 (tcp)'])
    def test_actualizar_ip_puertos(self, mock_puertos, mock_ip):
        self.widget.actualizar_ip_puertos()
        expected = "IP Pública: 192.168.1.1\nPuertos abiertos:\nPuerto 22 (tcp)\nPuerto 80 (tcp)"
        self.assertEqual(self.widget.datos_ip_puertos, expected)
        self.widget.label.setText.assert_called()

    @patch('ventana.red.listar_interfaces', return_value=['eth0', 'wlan0'])
    @patch('ventana.red.velocidad_por_interfaz', return_value={'eth0': {'enviados': 1000, 'recibidos': 2000}, 'wlan0': {'enviados': 500, 'recibidos': 1000}})
    def test_actualizar_red(self, mock_vel, mock_interfaces):
        self.widget.actualizar_red()
        expected = "Redes:\neth0: ↓ 2000 ↑ 1000\nwlan0: ↓ 1000 ↑ 500\n"
        self.assertEqual(self.widget.datos_red, expected)
        self.widget.label.setText.assert_called()

    @patch('ventana.procesos.procesos_principales', return_value=[(123, 'python', 15.5), (456, 'bash', 10.2)])
    @patch('ventana.servicios.estado_servicio')
    def test_actualizar_proc_serv(self, mock_serv, mock_proc):
        mock_serv.side_effect = lambda s: f"{s}: active"
        self.widget.actualizar_proc_serv()
        expected = "Procesos:\npython (15.5%)\nbash (10.2%)\n\nServicios:\nssh: active\napache2: active\nmysql: active"
        self.assertEqual(self.widget.datos_proc_serv, expected)
        self.widget.label.setText.assert_called()

    @patch('ventana.temperatura.temperatura_cpu', return_value='+45.0°C')
    @patch('ventana.memoria.memoria_ram', return_value='60% (512MB / 1024MB)')
    @patch('ventana.memoria.almacenamiento', return_value='75% usado (15GB / 20GB)')
    def test_actualizar_sistema(self, mock_disco, mock_ram, mock_temp):
        self.widget.actualizar_sistema()
        expected = "Temp CPU: +45.0°C\nRAM: 60% (512MB / 1024MB)\nDisco: 75% usado (15GB / 20GB)"
        self.assertEqual(self.widget.datos_sistema, expected)
        self.widget.label.setText.assert_called()

    def test_refrescar_widget(self):
        self.widget.datos_ip_puertos = "IP: test"
        self.widget.datos_red = "Red: test"
        self.widget.datos_sistema = "Sys: test"
        self.widget.datos_proc_serv = "Proc: test"
        self.widget.refrescar_widget()
        expected_text = "\n=== RaspKali Widget ===\nIP: test\n\nRed: test\n\nSys: test\n\nProc: test"
        self.widget.label.setText.assert_called_with(expected_text)

if __name__ == '__main__':
    unittest.main()