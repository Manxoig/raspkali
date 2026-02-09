RaspKali Widget Monitor
Un sistema de monitorización ligera para Kali Linux en Raspberry Pi, que muestra información crítica del sistema en un widget flotante siempre visible en el escritorio. Incluye gestión de logs configurable y actualización en intervalos diferenciados para optimizar recursos.

Requisitos del sistema
Sistema operativo: Kali Linux (adaptado para Raspberry Pi)

Hardware recomendado: Raspberry Pi 3 o superior (mejor rendimiento en Pi 4)

Entorno gráfico: XFCE, LXDE o cualquier entorno que soporte ventanas Tkinter

Python: versión 3.8 o superior

Dependencias de Python:

psutil (estadísticas de CPU, RAM, disco, red)

requests (IP pública y datos externos)

Paquetes adicionales:

lm-sensors (lectura de temperatura CPU)

systemd (estado de servicios)

curl (IP pública alternativa)

Instalación de dependencias
bash
sudo apt update
sudo apt install python3 python3-pip lm-sensors curl -y
pip3 install psutil requests
Configuración
Toda la configuración se realiza en el archivo config.ini.

Ejemplo de config.ini
ini
[logs]
# Opciones permitidas para retención:
# dia   -> conserva solo 24 horas de logs
# semana -> conserva 7 días de logs
# mes   -> conserva 30 días de logs
retencion = semana

[widget]
# Posición en pantalla (coordenadas X,Y)
posicion_x = 1200
posicion_y = 50

# Fuente y tamaño
fuente = DejaVu Sans Mono
tamano_fuente = 10

# Colores (usar nombres o códigos hexadecimales)
color_texto = lime
color_fondo = black

# Transparencia (0.0 = totalmente transparente, 1.0 = opaco)
transparencia = 0.85
Intervalos de actualización
Cada bloque de información se refresca con distinta frecuencia para optimizar recursos:

IP pública y puertos abiertos → cada 60 segundos

Redes (interfaces y tráfico) → cada 5 segundos

Procesos y servicios críticos → cada 5 minutos

Temperatura CPU, RAM y disco → cada 5 segundos

Gestión de logs
Los registros se guardan en la carpeta logs/ con un archivo por hora (YYYY-MM-DD-HH.log).

Cada archivo abarca 60 minutos de datos.

Cada entrada incluye una marca de tiempo y se separa con ---.

Los archivos más antiguos se eliminan automáticamente según la política configurada en config.ini (dia, semana, mes).

Ejecución
Dentro de la carpeta del proyecto:

bash
python3 ventana.py
El widget se abrirá y mostrará la información del sistema en tiempo real, flotando sobre el escritorio.

Autostart (opcional)
Para que el widget se ejecute automáticamente al iniciar el sistema:

Crea el archivo ~/.config/autostart/raspkali-widget.desktop

Contenido:

ini
[Desktop Entry]
Type=Application
Exec=python3 /ruta/al/proyecto/ventana.py
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
Name=RaspKali Widget
Comment=Monitor ligero para Raspberry Pi

Nota sobre validación de config.ini
El programa no se ejecutará si el archivo config.ini contiene valores inválidos o faltantes.
Antes de iniciar, se valida que:

retencion solo puede ser dia, semana o mes.

Los intervalos (intervalo_ip_puertos, intervalo_red, intervalo_proc_serv, intervalo_sistema) deben ser enteros positivos en segundos.

transparencia debe estar entre 0.0 y 1.0.

La fuente, colores y posición deben ser valores válidos para el sistema.

Si alguno de estos parámetros es incorrecto, el programa mostrará un mensaje de error indicando la opción inválida y se cerrará inmediatamente.
Esto garantiza que el widget no se ejecute con configuraciones defectuosas y evita comportamientos inesperados.