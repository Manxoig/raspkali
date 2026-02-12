RaspKali Widget Monitor
Un sistema de monitorización ligera para Kali Linux en Raspberry Pi, que muestra información crítica del sistema en un widget flotante siempre visible en el escritorio. Ahora implementado con PyQt5 para un estilo más moderno y configurable.

Prerrequisitos
Antes de instalar y ejecutar el widget, asegúrate de cumplir con lo siguiente:

Sistema operativo: Kali Linux (adaptado para Raspberry Pi)

Hardware recomendado: Raspberry Pi 3 o superior (mejor rendimiento en Pi 4)

Entorno gráfico: cualquier entorno que soporte aplicaciones PyQt5 (XFCE, LXDE, GNOME, etc.)

Python: versión 3.8 o superior

Dependencias de Python:

psutil → estadísticas de CPU, RAM, disco y red

requests → obtener IP pública y datos externos

PyQt5 → interfaz gráfica moderna

Paquetes adicionales del sistema:

lm-sensors → lectura de temperatura CPU

systemd → estado de servicios

curl → alternativa para IP pública

Instalación de dependencias
bash
sudo apt update
sudo apt install python3 python3-pip lm-sensors curl -y
pip3 install psutil requests PyQt5
Configuración
Toda la configuración se realiza en el archivo config.ini.

Ejemplo de config.ini
ini
[logs]
# Opciones permitidas: dia, semana, mes
retencion = semana

[widget]
posicion_x = 1200
posicion_y = 50
fuente = Consolas
tamano_fuente = 14
color_texto = #00FF00
color_fondo = #000000
transparencia = 0.85
alineacion = left

# Intervalos en segundos
intervalo_ip_puertos = 60
intervalo_red = 5
intervalo_proc_serv = 300
intervalo_sistema = 5
Validación de configuración
El programa valida config.ini antes de arrancar.
Si contiene valores inválidos o faltantes, muestra un mensaje de error en consola y se detiene.

Validaciones:

retencion debe ser dia, semana o mes.

Intervalos deben ser enteros positivos (en segundos).

transparencia debe estar entre 0.0 y 1.0.

Fuente, colores y posición deben ser valores válidos para el sistema.

Intervalos de actualización
IP pública y puertos abiertos → cada 60 segundos

Redes (interfaces y tráfico) → cada 5 segundos

Procesos y servicios críticos → cada 5 minutos

Temperatura CPU, RAM y disco → cada 5 segundos

Gestión de logs
Los registros se guardan en la carpeta logs/ con un archivo por hora (YYYY-MM-DD-HH.log).

Cada archivo abarca 60 minutos de datos.

Cada entrada incluye una marca de tiempo y se separa con ---.

Los archivos más antiguos se eliminan automáticamente según la política configurada en config.ini.

Ejecución
Dentro de la carpeta del proyecto:

bash
python3 ventana.py
El widget se abrirá y mostrará la información del sistema en tiempo real, flotando sobre el escritorio con estilo moderno gracias a PyQt5.

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
Comment=Monitor ligero para Raspberry Pi con PyQt5