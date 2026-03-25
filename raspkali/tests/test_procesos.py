import unittest
from raspkali_widget import procesos


class TestProcesos(unittest.TestCase):

    def test_procesos_principales_retorna_lista(self):
        result = procesos.procesos_principales(3)
        self.assertIsInstance(result, list)

    def test_procesos_principales_maximo_n(self):
        # Puede retornar menos de n si hay pocos procesos accesibles
        result = procesos.procesos_principales(3)
        self.assertLessEqual(len(result), 3)

    def test_procesos_principales_estructura_tupla(self):
        result = procesos.procesos_principales(3)
        for item in result:
            self.assertIsInstance(item, tuple)
            self.assertEqual(len(item), 3)
            pid, name, cpu = item
            self.assertIsInstance(pid, int)
            self.assertIsInstance(name, str)
            self.assertIsInstance(cpu, (int, float))

    def test_procesos_principales_ordenados_por_cpu(self):
        result = procesos.procesos_principales(5)
        cpus = [cpu for _, _, cpu in result]
        self.assertEqual(cpus, sorted(cpus, reverse=True))


if __name__ == '__main__':
    unittest.main()
