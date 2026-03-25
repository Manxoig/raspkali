#!/usr/bin/env python3
import unittest
import sys
import os

# Rutas actualizadas tras la refactorización del paquete
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'debian/usr/lib/python3/dist-packages'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'debian/usr/bin'))

if __name__ == '__main__':
    loader = unittest.TestLoader()
    suite = loader.discover('tests', pattern='test_*.py')
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)
