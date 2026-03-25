import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Mockear PyQt5 y raspkali_widget antes de importar ventana
# (ventana.py requiere display gráfico y config real en producción)
_qt = MagicMock()
for _mod in ['PyQt5', 'PyQt5.QtWidgets', 'PyQt5.QtCore', 'PyQt5.QtGui']:
    sys.modules[_mod] = _qt

_rw = MagicMock()
for _mod in ['raspkali_widget', 'raspkali_widget.procesos', 'raspkali_widget.servicios',
             'raspkali_widget.temperatura', 'raspkali_widget.memoria',
             'raspkali_widget.red', 'raspkali_widget.puertos']:
    sys.modules[_mod] = _rw

# Configurar entorno mínimo necesario para importar ventana
os.environ.setdefault('XDG_RUNTIME_DIR', '/tmp')

with patch('builtins.open', MagicMock()), \
     patch('os.access', return_value=True), \
     patch('pathlib.Path.exists', return_value=True):

    import configparser
    _cfg = configparser.ConfigParser()
    _cfg.read_dict({
        'logs':   {'retencion': 'semana'},
        'widget': {
            'posicion_x': '0', 'posicion_y': '0',
            'fuente': 'Monospace', 'tamano_fuente': '12',
            'color_texto': '#00FF00', 'color_fondo': '#000000',
            'transparencia': '0.85', 'alineacion': 'left',
            'obtener_ip_publica': 'false', 'servicios': 'ssh',
            'intervalo_ip_puertos': '60', 'intervalo_red': '5',
            'intervalo_proc_serv': '300', 'intervalo_sistema': '5',
        }
    })

    with patch('configparser.ConfigParser', return_value=_cfg):
        import ventana


class TestCallbacksWidget(unittest.TestCase):
    """Prueba los métodos _on_* que actualizan el estado del widget."""

    def _make_widget(self):
        w = MagicMock(spec=ventana.RaspKaliWidget)
        w.datos_ip_puertos = ""
        w.datos_red = ""
        w.datos_proc_serv = ""
        w.datos_sistema = ""
        w.label = MagicMock()
        w.refrescar_widget = MagicMock()
        return w

    def test_on_ip_puertos_desactivado(self):
        w = self._make_widget()
        ventana.RaspKaliWidget._on_ip_puertos(w, 'desactivado', 'Ninguno')
        self.assertIn('desactivado', w.datos_ip_puertos)
        w.refrescar_widget.assert_called_once()

    def test_on_ip_puertos_con_ip(self):
        w = self._make_widget()
        ventana.RaspKaliWidget._on_ip_puertos(w, '1.2.3.4', 'Puerto 22\nPuerto 80')
        self.assertIn('1.2.3.4', w.datos_ip_puertos)
        self.assertIn('Puerto 22', w.datos_ip_puertos)

    def test_on_red(self):
        w = self._make_widget()
        ventana.RaspKaliWidget._on_red(w, 'eth0: ↓ 1.0 KB/s ↑ 512 B/s\n')
        self.assertIn('eth0', w.datos_red)
        w.refrescar_widget.assert_called_once()

    def test_on_proc_serv(self):
        w = self._make_widget()
        ventana.RaspKaliWidget._on_proc_serv(w, 'python (15.5%)', 'ssh: active')
        self.assertIn('python', w.datos_proc_serv)
        self.assertIn('ssh', w.datos_proc_serv)
        w.refrescar_widget.assert_called_once()

    def test_on_sistema(self):
        w = self._make_widget()
        ventana.RaspKaliWidget._on_sistema(w, '+45.0°C', '60% (512MB / 1024MB)', '75% usado')
        self.assertIn('+45.0°C', w.datos_sistema)
        self.assertIn('60%', w.datos_sistema)
        w.refrescar_widget.assert_called_once()

    def test_refrescar_widget_formato(self):
        w = self._make_widget()
        w.datos_ip_puertos = "IP: test"
        w.datos_red = "Red: test"
        w.datos_sistema = "Sys: test"
        w.datos_proc_serv = "Proc: test"
        ventana.RaspKaliWidget.refrescar_widget(w)
        w.label.setText.assert_called_once()
        texto = w.label.setText.call_args[0][0]
        self.assertIn('RaspKali Widget', texto)
        self.assertIn('IP: test', texto)
        self.assertIn('Red: test', texto)


if __name__ == '__main__':
    unittest.main()
