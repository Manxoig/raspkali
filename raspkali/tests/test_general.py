import unittest
from unittest.mock import MagicMock


class TestImports(unittest.TestCase):
    """Verifica que todos los módulos del paquete son importables."""

    def test_importar_memoria(self):
        from raspkali_widget import memoria
        self.assertTrue(callable(memoria.memoria_ram))
        self.assertTrue(callable(memoria.almacenamiento))

    def test_importar_procesos(self):
        from raspkali_widget import procesos
        self.assertTrue(callable(procesos.procesos_principales))

    def test_importar_puertos(self):
        from raspkali_widget import puertos
        self.assertTrue(callable(puertos.puertos_abiertos))

    def test_importar_red(self):
        from raspkali_widget import red
        self.assertTrue(callable(red.obtener_ip_publica))
        self.assertTrue(callable(red.listar_interfaces))
        self.assertTrue(callable(red.velocidad_por_interfaz))

    def test_importar_servicios(self):
        from raspkali_widget import servicios
        self.assertTrue(callable(servicios.estado_servicio))

    def test_importar_temperatura(self):
        from raspkali_widget import temperatura
        self.assertTrue(callable(temperatura.temperatura_cpu))

    def test_version_definida(self):
        import raspkali_widget
        self.assertTrue(hasattr(raspkali_widget, '__version__'))
        self.assertIsInstance(raspkali_widget.__version__, str)


if __name__ == '__main__':
    unittest.main()
