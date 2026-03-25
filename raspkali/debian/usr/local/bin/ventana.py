#!/usr/bin/env python3
import sys
import os
import glob
from datetime import datetime, timedelta
from pathlib import Path
import configparser

# PyQt5
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QColor, QPalette

# Módulos del paquete widget
from widget import procesos, servicios, temperatura, memoria, red, puertos

# -------------------------
# Buscar y cargar config.ini
# -------------------------
def find_config():
    # 1) Variable de entorno para forzar ruta en desarrollo
    env = os.getenv("RASPKALI_CONFIG")
    if env:
        p = Path(env).resolve()
        print(f"RASPKALI_CONFIG definido: {p}")
        if p.exists() and os.access(p, os.R_OK):
            return p
        print(f"RASPKALI_CONFIG no válido o sin permisos: {p}")

    # 2) Rutas candidatas (prioridad)
    candidates = [
        Path("/etc/raspkali-widget/config.ini").resolve(),
    ]

    print("Rutas probadas para config.ini (en orden):")
    for c in candidates:
        print(f"  - {c}")

    for p in candidates:
        try:
            if p.exists():
                if os.access(p, os.R_OK):
                    print(f"Encontrado y legible: {p}")
                    return p
                else:
                    print(f"Encontrado pero sin permisos de lectura: {p}")
        except Exception as e:
            print(f"Error comprobando {p}: {e}")

    print("No se encontró config.ini en las rutas probadas.")
    return None

config_path = find_config()
if not config_path:
    sys.exit(1)

print(f"Usando config.ini en: {config_path}")
config = configparser.ConfigParser()
read_list = config.read(str(config_path))
print("configparser.read devolvió:", read_list)
print("Secciones encontradas en config.ini:", config.sections())
if not read_list:
    print(f"Error: configparser no pudo leer {config_path}")
    sys.exit(1)

# -------------------------
# Validar configuración
# -------------------------
def validar_config():
    retencion = config.get("logs", "retencion", fallback=None)
    if retencion not in ["dia", "semana", "mes"]:
        print("Error en config.ini: 'retencion' debe ser 'dia', 'semana' o 'mes'")
        sys.exit(1)

    for clave in ["intervalo_ip_puertos", "intervalo_red", "intervalo_proc_serv", "intervalo_sistema"]:
        try:
            valor = config.getint("widget", clave)
            if valor <= 0:
                raise ValueError
        except Exception:
            print(f"Error en config.ini: '{clave}' debe ser un número entero positivo")
            sys.exit(1)

    try:
        trans = config.getfloat("widget", "transparencia")
        if not (0.0 <= trans <= 1.0):
            raise ValueError
    except Exception:
        print("Error en config.ini: 'transparencia' debe estar entre 0.0 y 1.0")
        sys.exit(1)

validar_config()

# -------------------------
# Constantes desde config
# -------------------------
RETENCION = config.get("logs", "retencion")
POS_X = config.getint("widget", "posicion_x")
POS_Y = config.getint("widget", "posicion_y")
FUENTE = config.get("widget", "fuente")
TAMANO = config.getint("widget", "tamano_fuente")
COLOR_TEXTO = config.get("widget", "color_texto")
COLOR_FONDO = config.get("widget", "color_fondo")
TRANSPARENCIA = config.getfloat("widget", "transparencia")
ALINEACION = config.get("widget", "alineacion", fallback="left")

INTERVALO_IP_PUERTOS = config.getint("widget", "intervalo_ip_puertos") * 1000
INTERVALO_RED = config.getint("widget", "intervalo_red") * 1000
INTERVALO_PROC_SERV = config.getint("widget", "intervalo_proc_serv") * 1000
INTERVALO_SISTEMA = config.getint("widget", "intervalo_sistema") * 1000

# Logs
LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR, exist_ok=True)

def obtener_limite_retencion():
    ahora = datetime.now()
    if RETENCION == "dia":
        return ahora - timedelta(days=1)
    elif RETENCION == "semana":
        return ahora - timedelta(weeks=1)
    elif RETENCION == "mes":
        return ahora - timedelta(days=30)
    return ahora

def limpiar_logs():
    limite = obtener_limite_retencion()
    for archivo in glob.glob(os.path.join(LOG_DIR, "*.log")):
        fecha_str = os.path.basename(archivo).split(".")[0]
        try:
            fecha = datetime.strptime(fecha_str, "%Y-%m-%d-%H")
            if fecha < limite:
                os.remove(archivo)
        except Exception:
            pass

def guardar_registro(texto):
    nombre = datetime.now().strftime("%Y-%m-%d-%H") + ".log"
    ruta = os.path.join(LOG_DIR, nombre)
    with open(ruta, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]\n{texto}\n---\n")
    limpiar_logs()

# -------------------------
# Widget PyQt
# -------------------------
class RaspKaliWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(POS_X, POS_Y, 400, 300)
        self.setWindowOpacity(TRANSPARENCIA)

        layout = QVBoxLayout()
        self.label = QLabel("Cargando datos...")
        self.label.setFont(QFont(FUENTE, TAMANO))
        self.label.setStyleSheet(f"color: {COLOR_TEXTO}; background-color: {COLOR_FONDO};")
        if ALINEACION == "center":
            self.label.setAlignment(Qt.AlignCenter)
        elif ALINEACION == "right":
            self.label.setAlignment(Qt.AlignRight)
        else:
            self.label.setAlignment(Qt.AlignLeft)
        layout.addWidget(self.label)
        self.setLayout(layout)

        # Timers
        self.timer_ip = QTimer(self)
        self.timer_ip.timeout.connect(self.actualizar_ip_puertos)
        self.timer_ip.start(INTERVALO_IP_PUERTOS)

        self.timer_red = QTimer(self)
        self.timer_red.timeout.connect(self.actualizar_red)
        self.timer_red.start(INTERVALO_RED)

        self.timer_proc = QTimer(self)
        self.timer_proc.timeout.connect(self.actualizar_proc_serv)
        self.timer_proc.start(INTERVALO_PROC_SERV)

        self.timer_sys = QTimer(self)
        self.timer_sys.timeout.connect(self.actualizar_sistema)
        self.timer_sys.start(INTERVALO_SISTEMA)

        # Datos iniciales
        self.datos_ip_puertos = ""
        self.datos_red = ""
        self.datos_proc_serv = ""
        self.datos_sistema = ""

    def refrescar_widget(self):
        texto = f"""
=== RaspKali Widget ===
{self.datos_ip_puertos}

{self.datos_red}

{self.datos_sistema}

{self.datos_proc_serv}
"""
        self.label.setText(texto)

    def actualizar_ip_puertos(self):
        try:
            ip = red.obtener_ip_publica()
        except Exception:
            ip = "N/A"
        try:
            puertos_text = "\n".join(puertos.puertos_abiertos())
        except Exception:
            puertos_text = "N/A"
        self.datos_ip_puertos = f"IP Pública: {ip}\nPuertos abiertos:\n{puertos_text}"
        self.refrescar_widget()
        guardar_registro(self.datos_ip_puertos)

    def actualizar_red(self):
        try:
            interfaces = red.listar_interfaces()
            velocidades = red.velocidad_por_interfaz()
        except Exception:
            interfaces = []
            velocidades = {}
        vel_text = ""
        for iface in interfaces:
            if iface in velocidades:
                v = velocidades[iface]
                vel_text += f"{iface}: ↓ {v.get('recibidos','?')} ↑ {v.get('enviados','?')}\n"
        self.datos_red = f"Redes:\n{vel_text}"
        self.refrescar_widget()
        guardar_registro(self.datos_red)

    def actualizar_proc_serv(self):
        try:
            top_proc = procesos.procesos_principales(3)
            proc_text = "\n".join([f"{name} ({cpu}%)" for name, cpu in top_proc])
        except Exception:
            proc_text = "N/A"
        servicios_list = ["ssh", "apache2", "mysql"]
        try:
            serv_text = "\n".join([servicios.estado_servicio(s) for s in servicios_list])
        except Exception:
            serv_text = "N/A"
        self.datos_proc_serv = f"Procesos:\n{proc_text}\n\nServicios:\n{serv_text}"
        self.refrescar_widget()
        guardar_registro(self.datos_proc_serv)

    def actualizar_sistema(self):
        try:
            temp = temperatura.temperatura_cpu()
        except Exception:
            temp = "N/A"
        try:
            ram = memoria.memoria_ram()
            disco = memoria.almacenamiento()
        except Exception:
            ram = "N/A"
            disco = "N/A"
        self.datos_sistema = f"Temp CPU: {temp}\nRAM: {ram}\nDisco: {disco}"
        self.refrescar_widget()
        guardar_registro(self.datos_sistema)

# -------------------------
# Main
# -------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = RaspKaliWidget()
    ventana.show()
    sys.exit(app.exec_())