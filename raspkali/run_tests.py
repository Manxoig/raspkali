#!/usr/bin/env python3
# Script para ejecutar todos los tests
import unittest
import sys
import os

# Agregar el directorio del paquete al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'debian/usr/lib'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'debian/usr/local/bin'))

if __name__ == '__main__':
    # Descubrir y ejecutar tests
    loader = unittest.TestLoader()
    suite = loader.discover('tests', pattern='test_*.py')
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)