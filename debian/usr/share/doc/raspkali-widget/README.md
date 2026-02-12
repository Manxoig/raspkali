
</head>
<body>

  <h1>📦 RaspKali Widget Monitor (.deb)</h1>
  <p>Este proyecto se distribuye como un <strong>paquete Debian (.deb)</strong> para instalarse fácilmente en sistemas basados en <strong>Debian/Ubuntu/Kali</strong>.</p>

  <div class="section">
    <h2>🔧 Prerrequisitos para empaquetado</h2>
    <p>Antes de generar el paquete <code>.deb</code>, asegúrate de tener instaladas las siguientes herramientas:</p>
    <ul>
      <li><strong>dpkg-deb</strong> → construcción de paquetes .deb</li>
      <li><strong>fakeroot</strong> → simular permisos de root durante la construcción</li>
      <li><strong>build-essential</strong> → compiladores y utilidades básicas</li>
      <li><strong>lintian</strong> → verificación de calidad del paquete</li>
    </ul>
    <h3>Instalación de herramientas</h3>
    <pre><code>sudo apt update
sudo apt install dpkg-dev fakeroot build-essential lintian -y</code></pre>
  </div>

  <div class="section">
    <h2>📂 Estructura del paquete</h2>
    <pre><code>raspkali-widget/
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
                └── README.md</code></pre>
  </div>

  <div class="section">
    <h2>📑 Archivo <code>control</code></h2>
    <pre><code>Package: raspkali-widget
Version: 1.0
Section: utils
Priority: optional
Architecture: all
Depends: python3, python3-psutil, python3-requests, python3-pyqt5, lm-sensors, curl
Maintainer: Tu Nombre &lt;tuemail@example.com&gt;
Description: RaspKali Widget Monitor
 Un widget flotante para monitorizar CPU, RAM, disco, red y servicios en Raspberry Pi con Kali Linux.
 Implementado en PyQt5, configurable mediante config.ini y con gestión de logs automática.</code></pre>
  </div>

  <div class="section">
    <h2>⚙️ Explicación de <code>config.ini</code></h2>
    <p>El archivo <code>config.ini</code> define cómo se comporta el widget. Se instala en:</p>
    <pre><code>/etc/raspkali-widget/config.ini</code></pre>

    <h3>Secciones y parámetros</h3>
    <ul>
      <li><strong>[logs]</strong>
        <ul>
          <li><code>retencion</code>: controla cuánto tiempo se conservan los logs. Valores: <code>dia</code>, <code>semana</code>, <code>mes</code>.</li>
        </ul>
      </li>
      <li><strong>[widget]</strong>
        <ul>
          <li><code>posicion_x</code>, <code>posicion_y</code>: coordenadas en pantalla.</li>
          <li><code>fuente</code>: nombre de la fuente (ej. Consolas).</li>
          <li><code>tamano_fuente</code>: tamaño de la fuente en puntos.</li>
          <li><code>color_texto</code>: color del texto (nombre o hex).</li>
          <li><code>color_fondo</code>: color de fondo.</li>
          <li><code>transparencia</code>: valor entre 0.0 y 1.0.</li>
          <li><code>alineacion</code>: alineación del texto (left, center, right).</li>
          <li><code>intervalo_ip_puertos</code>: segundos entre actualizaciones de IP y puertos.</li>
          <li><code>intervalo_red</code>: segundos entre actualizaciones de red.</li>
          <li><code>intervalo_proc_serv</code>: segundos entre actualizaciones de procesos y servicios.</li>
          <li><code>intervalo_sistema</code>: segundos entre actualizaciones de CPU, RAM y disco.</li>
        </ul>
      </li>
    </ul>
  </div>

  <div class="section">
    <h2>🛠️ Construcción del paquete</h2>
    <ol>
      <li>Crear la estructura de directorios como se muestra arriba.</li>
      <li>Copiar los archivos en sus rutas correspondientes.</li>
      <li>Dar permisos de ejecución al script principal:
        <pre><code>chmod 755 usr/local/bin/ventana.py</code></pre>
      </li>
      <li>Construir el paquete:
        <pre><code>dpkg-deb --build raspkali-widget</code></pre>
      </li>
      <li>Verificar con lintian:
        <pre><code>lintian raspkali-widget.deb</code></pre>
      </li>
    </ol>
  </div>

  <div class="section">
    <h2>🚀 Instalación del paquete</h2>
    <pre><code>sudo dpkg -i raspkali-widget.deb
sudo apt-get install -f</code></pre>
    <p>Esto instalará el widget en el sistema con sus dependencias y rutas correctas.</p>
  </div>

</body>
</html>
