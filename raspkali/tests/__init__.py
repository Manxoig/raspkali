import sys
import os

# Añadir rutas del paquete para todos los tests
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'debian/usr/lib/python3/dist-packages'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'debian/usr/bin'))
