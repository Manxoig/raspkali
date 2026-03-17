<!DOCTYPE html>
<html lang="es">
<body style="font-family: Consolas, monospace; background-color: #121212; color: #e0e0e0; line-height: 1.6; margin: 20px;">

  <h1 style="color:#00ff7f; border-bottom:1px solid #333; padding-bottom:5px;">📦 RaspKali Widget Monitor (.deb)</h1>
  <p>Este proyecto se distribuye como un <strong style="color:#ffcc00;">paquete Debian (.deb)</strong> para instalarse fácilmente en sistemas basados en <strong>Debian/Ubuntu/Kali</strong>.</p>

  <div style="margin-bottom:40px;">
    <h2 style="color:#00ff7f;">🔧 Prerrequisitos para empaquetado</h2>
    <p>Antes de generar el paquete <code>.deb</code>, asegúrate de tener instaladas las siguientes herramientas:</p>
    <ul style="list-style-type:none; padding-left:0;">
      <li style="margin-bottom:5px;">✔ <strong>dpkg-deb</strong> → construcción de paquetes .deb</li>
      <li style="margin-bottom:5px;">✔ <strong>fakeroot</strong> → simular permisos de root durante la construcción</li>
      <li style="margin-bottom:5px;">✔ <strong>build-essential</strong> → compiladores y utilidades básicas</li>
      <li style="margin-bottom:5px;">✔ <strong>lintian</strong> → verificación de calidad del paquete</li>
    </ul>
    <pre style="background-color:#1e1e1e; color:#00ff7f; padding:12px; border-radius:5px;">
sudo apt update
sudo apt install dpkg-dev fakeroot build-essential lintian -y
    </pre>
  </div>

  <div style="margin-bottom:40px;">
    <h2 style="color:#00ff7f;">📂 Estructura del paquete</h2>
    <pre style="background-color:#1e1e1e; color:#00ff7f; padding:12px; border-radius:5px;">
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
    </pre>
  </div>

  <div style="margin-bottom:40px;">
    <h2 style="color:#00ff7f;">📑 Archivo <code>control</code></h2>
    <pre style="background-color:#1e1e1e; color:#00ff7f; padding:12px; border-radius:5px;">
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
    </pre>
  </div>

<h2 style="color:#00ff7f;">⚙️ Explicación de <code>config.ini</code></h2>
<p>El archivo <code>config.ini</code> define cómo se comporta el widget. Se instala en:</p>
<pre style="background-color:#1e1e1e; color:#00ff7f; padding:12px; border-radius:5px;">/etc/raspkali-widget/config.ini</pre>

<h3 style="color:#ffcc00;">Secciones y parámetros</h3>
<ul style="list-style-type:none; padding-left:0;">
  <li>✓ <strong>[logs]</strong>
    <ul>
      <li><code>retencion</code>: controla cuánto tiempo se conservan los logs. Valores: <code>dia</code>, <code>semana</code>, <code>mes</code>.</li>
    </ul>
  </li>
  <li>✓ <strong>[widget]</strong>
    <ul>
      <li><em>Posición y estilo:</em></li>
      <li><code>posicion_x</code>, <code>posicion_y</code>: coordenadas en pantalla.</li>
      <li><code>fuente</code>: nombre de la fuente (ej. Consolas).</li>
      <li><code>tamano_fuente</code>: tamaño de la fuente en puntos.</li>
      <li><code>color_texto</code>: color del texto (ej. #00FF00).</li>
      <li><code>color_fondo</code>: color de fondo (ej. #000000).</li>
      <li><code>transparencia</code>: valor entre 0.0 y 1.0.</li>
      <li><code>alineacion</code>: alineación del texto (left, center, right).</li>
      <br>
      <li><em>Intervalos de actualización:</em></li>
      <li><code>intervalo_ip_puertos</code>: segundos entre actualizaciones de IP y puertos.</li>
      <li><code>intervalo_red</code>: segundos entre actualizaciones de red.</li>
      <li><code>intervalo_proc_serv</code>: segundos entre actualizaciones de procesos y servicios.</li>
      <li><code>intervalo_sistema</code>: segundos entre actualizaciones de CPU, RAM y disco.</li>
    </ul>
  </li>
</ul>


  <div style="margin-bottom:40px;">
    <h2 style="color:#00ff7f;">🛠️ Construcción del paquete</h2>
    <p>Usa el <code>Makefile</code> para automatizar la construcción:</p>
    <pre style="background-color:#1e1e1e; color:#00ff7f; padding:12px; border-radius:5px;">
make build    # Construir raspkali-widget.deb
make check    # Verificar con lintian
make test     # Ejecutar tests
make all      # Todo lo anterior
make install  # Instalar el paquete
make clean    # Limpiar
    </pre>
    <p>O manualmente:</p>
    <ol>
      <li>Crear la estructura de directorios como se muestra arriba.</li>
      <li>Copiar los archivos en sus rutas correspondientes.</li>
      <li>Dar permisos de ejecución al script principal:
        <pre style="background-color:#1e1e1e; color:#00ff7f; padding:12px; border-radius:5px;">chmod 755 usr/local/bin/ventana.py</pre>
      </li>
      <li>Construir el paquete:
        <pre style="background-color:#1e1e1e; color:#00ff7f; padding:12px; border-radius:5px;">dpkg-deb --build raspkali-widget</pre>
      </li>
      <li>Verificar con lintian:
        <pre style="background-color:#1e1e1e; color:#00ff7f; padding:12px; border-radius:5px;">lintian raspkali-widget.deb</pre>
      </li>
    </ol>
  </div>

  <div style="margin-bottom:40px;">
    <h2 style="color:#00ff7f;">🚀 Instalación del paquete</h2>
    <pre style="background-color:#1e1e1e; color:#00ff7f; padding:12px; border-radius:5px;">
sudo dpkg -i raspkali-widget.deb
sudo apt-get install -f
    </pre>
    <p>Esto instalará el widget en el sistema con sus dependencias y rutas correctas.</p>
  </div>

</body>
</html>
