import unittest
from widget import procesos

class TestProcesos(unittest.TestCase):
    def test_procesos_principales(self):
        result = procesos.procesos_principales(3)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 3)
        for item in result:
            self.assertIsInstance(item, tuple)
            self.assertEqual(len(item), 3)
            pid, name, cpu = item
            self.assertIsInstance(pid, int)
            self.assertIsInstance(name, str)
            self.assertIsInstance(cpu, (int, float))

if __name__ == '__main__':
    unittest.main()