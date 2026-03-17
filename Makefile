# Makefile para construir el paquete RaspKali Widget

.PHONY: all build clean install test

# Construir el paquete .deb
build:
	dpkg-deb --build raspkali/debian
	mv raspkali/debian.deb raspkali-widget.deb

# Verificar el paquete con lintian
check: build
	lintian raspkali-widget.deb

# Limpiar archivos generados
clean:
	rm -f raspkali-widget.deb
	rm -rf raspkali/debian/var/log/raspkali-widget/*
	rm -rf logs/

# Instalar el paquete (requiere sudo)
install: build
	sudo dpkg -i raspkali-widget.deb
	sudo apt-get install -f

# Ejecutar tests
test:
	python3 run_tests.py

# Todo: build, check, test
all: build check test

# Ayuda
help:
	@echo "Comandos disponibles:"
	@echo "  make build    - Construir el paquete .deb"
	@echo "  make check    - Verificar el paquete con lintian"
	@echo "  make clean    - Limpiar archivos generados"
	@echo "  make install  - Instalar el paquete"
	@echo "  make test     - Ejecutar tests"
	@echo "  make all      - Construir, verificar y testear"