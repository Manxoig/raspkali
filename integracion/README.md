# raspkali
RaspKali es una adaptación de Kali Linux para Raspberry Pi. Cada uno de los códigos disponibles sirve para reparar el sistema de forma independiente o conjunta, después de usar ciertas características como wifite.

El uso de wifite se presenta en una forma web minimalista. Como requiere conexión a internet, también debe poder ejecutarse de manera local para funcionar correctamente.
Un detalle importante: al usar wifite en Raspberry Pi, la conexión Wi-Fi puede dañarse o interrumpirse. Por ello, lo más lógico es utilizar eth0 (Ethernet) para mantener la comunicación, ya que de lo contrario te desconectarías y no podrías seguir trabajando, a menos que uses dos antenas simultáneamente.

La versión 0.2 incluirá una serie de utilidades preinstaladas accesibles vía web.

Funciones incluidas
Mostrar tu IP pública

Mostrar la temperatura de la CPU

Mostrar la memoria RAM y almacenamiento disponible

Requisitos del sistema
Para ejecutar RaspKali Monitor necesitas:

Sistema operativo: Kali Linux (adaptado para Raspberry Pi)
Hardware: Raspberry Pi 3 o superior (se recomienda Pi 4 para mejor rendimiento)
Entorno gráfico: XFCE, LXDE o cualquier entorno que soporte ventanas Tkinter
Python: versión 3.8 o superior
Dependencias de Python:
    psutil (para estadísticas de CPU, RAM y disco)
    requests (para obtener la IP pública y datos externos)
Paquetes adicionales:
    lm-sensors (para leer la temperatura de la CPU)
    systemd (para verificar estado de servicios)
    curl (para obtener IP pública si no se usa Python requests)
Instalación de dependencias
Ejecuta los siguientes comandos en tu Raspberry Pi:

sudo apt update
sudo apt install python3 python3-pip lm-sensors curl -y
pip3 install psutil requests