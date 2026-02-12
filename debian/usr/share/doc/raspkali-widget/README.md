📦 RaspKali Widget Monitor (.deb)
Este proyecto se distribuye como un paquete Debian (.deb) para instalarse fácilmente en sistemas basados en Debian/Ubuntu/Kali.

🔧 Prerrequisitos para empaquetado
Antes de generar el paquete .deb, asegúrate de tener instaladas las siguientes herramientas:

dpkg-deb → construcción de paquetes .deb

fakeroot → simular permisos de root durante la construcción

build-essential → compiladores y utilidades básicas

lintian → verificación de calidad del paquete

Instalación de herramientas
bash
sudo apt update
sudo apt install dpkg-dev fakeroot build-essential lintian -y
📂 Estructura del paquete
La estructura recomendada es:

Código
raspkali-widget/
├── DEBIAN/
│   └── control
├── usr/
│   ├── local/
│   │   └── bin/
│   │       └── ventana.py
│   └── lib/
│       └── raspkali-widget/
│           ├── memoria.py
│           ├── procesos.py
│           ├── puertos.py
│           ├── red.py
│           ├── servicios.py
│           └── temperatura.py
├── etc/
│   └── raspkali-widget/
│       └── config.ini
├── var/
│   └── log/
│       └── raspkali-widget/
└── usr/
    └── share/
        └── doc/
            └── raspkali-widget/
                └── README.md
📑 Archivo control
Ejemplo de DEBIAN/control:

text
Package: raspkali-widget
Version: 1.0
Section: utils
Priority: optional
Architecture: all
Depends: python3, python3-psutil, python3-requests, python3-pyqt5, lm-sensors, curl
Maintainer: Tu Nombre <tuemail@example.com>
Description: RaspKali Widget Monitor
 Un widget flotante para monitorizar CPU, RAM, disco, red y servicios en Raspberry Pi con Kali Linux.
 Implementado en PyQt5, configurable mediante config.ini y con gestión de logs automática.
⚙️ Explicación de config.ini
El archivo config.ini define cómo se comporta el widget. Se instala en:

Código
/etc/raspkali-widget/config.ini
Secciones y parámetros
[logs]

retencion: controla cuánto tiempo se conservan los logs.
Valores permitidos: dia, semana, mes.

[widget]

posicion_x, posicion_y: coordenadas en pantalla donde aparece el widget.

fuente: nombre de la fuente usada (ej. Consolas).

tamano_fuente: tamaño de la fuente en puntos.

color_texto: color del texto (nombre o código hex).

color_fondo: color de fondo del widget.

transparencia: valor entre 0.0 y 1.0 (0 = transparente, 1 = opaco).

alineacion: alineación del texto (left, center, right).

intervalo_ip_puertos: segundos entre actualizaciones de IP y puertos.

intervalo_red: segundos entre actualizaciones de red.

intervalo_proc_serv: segundos entre actualizaciones de procesos y servicios.

intervalo_sistema: segundos entre actualizaciones de CPU, RAM y disco.

🛠️ Construcción del paquete
Crear la estructura de directorios como se muestra arriba.

Copiar los archivos en sus rutas correspondientes.

Dar permisos de ejecución al script principal:

bash
chmod 755 usr/local/bin/ventana.py
Construir el paquete:

bash
dpkg-deb --build raspkali-widget
Verificar con lintian:

bash
lintian raspkali-widget.deb
🚀 Instalación del paquete
En cualquier sistema Debian/Ubuntu/Kali:

bash
sudo dpkg -i raspkali-widget.deb
sudo apt-get install -f
Esto instalará el widget en el sistema con sus dependencias y rutas correctas.
sudo dpkg -i raspkali-widget.deb
sudo apt-get install -f
Esto instalará el widget en el sistema con sus dependencias y rutas correctas.
