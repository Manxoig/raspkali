#!/usr/bin/env python3
import sys
import os
import glob
import signal
import atexit
import logging
import re
from datetime import datetime, timedelta
from pathlib import Path
import configparser

# -------------------------
# Logging (conforme a Debian Policy — stderr, sin fichero propio)
# -------------------------
logging.basicConfig(
    stream=sys.stderr,
    level=logging.INFO,
    format="%(asctime)s %(name)s %(levelname)s: %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)
log = logging.getLogger("raspkali-widget")

# -------------------------
# PID file (XDG_RUNTIME_DIR es estándar en Ubuntu/systemd)
# -------------------------
_xdg = os.environ.get("XDG_RUNTIME_DIR")
if not _xdg:
    log.critical("XDG_RUNTIME_DIR no definido — ejecutar desde una sesión de escritorio")
    sys.exit(1)
_PID_FILE = Path(_xdg) / "raspkali-widget.pid"

def _escribir_pid():
    _PID_FILE.write_text(str(os.getpid()))

def _eliminar_pid():
    if _PID_FILE.exists():
        _PID_FILE.unlink(missing_ok=True)

# PyQt5
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt, QTimer, QThread, QObject, pyqtSignal
from PyQt5.QtGui import QFont

# Módulos del paquete widget
from raspkali_widget import procesos, servicios, temperatura, memoria, red, puertos

# -------------------------
# Buscar y cargar config.ini
# -------------------------
def find_config():
    env = os.getenv("RASPKALI_CONFIG")
    if env:
        p = Path(env).resolve()
        log.debug("RASPKALI_CONFIG definido: %s", p)
        if p.exists() and os.access(p, os.R_OK):
            return p
        log.warning("RASPKALI_CONFIG no válido o sin permisos: %s", p)

    candidates = [Path("/etc/raspkali-widget/config.ini").resolve()]
    log.debug("Rutas probadas para config.ini: %s", candidates)

    for p in candidates:
        try:
            if p.exists():
                if os.access(p, os.R_OK):
                    log.info("config.ini encontrado: %s", p)
                    return p
                else:
                    log.warning("config.ini sin permisos de lectura: %s", p)
        except Exception as e:
            log.error("Error comprobando %s: %s", p, e)

    log.critical("No se encontró config.ini en las rutas probadas.")
    return None

config_path = find_config()
if not config_path:
    sys.exit(1)

log.info("Usando config.ini en: %s", config_path)
config = configparser.ConfigParser()
read_list = config.read(str(config_path))
log.debug("configparser.read devolvió: %s", read_list)
log.debug("Secciones encontradas: %s", config.sections())
if not read_list:
    log.critical("configparser no pudo leer %s", config_path)
    sys.exit(1)

# -------------------------
# Validar configuración
# -------------------------
def validar_config():
    retencion = config.get("logs", "retencion", fallback=None)
    if retencion not in ["dia", "semana", "mes"]:
        log.critical("config.ini: 'retencion' debe ser 'dia', 'semana' o 'mes'")
        sys.exit(1)

    for clave in ["intervalo_ip_puertos", "intervalo_red", "intervalo_proc_serv", "intervalo_sistema"]:
        try:
            valor = config.getint("widget", clave)
            if valor <= 0:
                raise ValueError
        except Exception:
            log.critical("config.ini: '%s' debe ser un número entero positivo", clave)
            sys.exit(1)

    try:
        trans = config.getfloat("widget", "transparencia")
        if not (0.0 <= trans <= 1.0):
            raise ValueError
    except Exception:
        log.critical("config.ini: 'transparencia' debe estar entre 0.0 y 1.0")
        sys.exit(1)

    try:
        config.getboolean("widget", "obtener_ip_publica")
    except (ValueError, configparser.NoOptionError):
        log.critical("config.ini: 'obtener_ip_publica' debe ser true o false")
        sys.exit(1)

    _hex_re = re.compile(r'^#([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$')
    for clave in ["color_texto", "color_fondo"]:
        valor = config.get("widget", clave, fallback="")
        if not _hex_re.match(valor):
            log.critical("config.ini: '%s' debe ser un color hex válido (#RGB o #RRGGBB)", clave)
            sys.exit(1)

validar_config()

# -------------------------
# Constantes desde config
# -------------------------
RETENCION          = config.get("logs", "retencion")
POS_X              = config.getint("widget", "posicion_x")
POS_Y              = config.getint("widget", "posicion_y")
FUENTE             = config.get("widget", "fuente")
TAMANO             = config.getint("widget", "tamano_fuente")
COLOR_TEXTO        = config.get("widget", "color_texto")
COLOR_FONDO        = config.get("widget", "color_fondo")
TRANSPARENCIA      = config.getfloat("widget", "transparencia")
ALINEACION         = config.get("widget", "alineacion", fallback="left")
OBTENER_IP_PUBLICA = config.getboolean("widget", "obtener_ip_publica", fallback=False)

INTERVALO_IP_PUERTOS = config.getint("widget", "intervalo_ip_puertos") * 1000
INTERVALO_RED        = config.getint("widget", "intervalo_red") * 1000
INTERVALO_PROC_SERV  = config.getint("widget", "intervalo_proc_serv") * 1000
INTERVALO_SISTEMA    = config.getint("widget", "intervalo_sistema") * 1000
SERVICIOS            = [s.strip() for s in config.get("widget", "servicios", fallback="ssh").split(",") if s.strip()]

# -------------------------
# Logs
# -------------------------
LOG_DIR = "/var/log/raspkali-widget"
if not os.access(LOG_DIR, os.W_OK):
    log.critical("%s no existe o no tiene permisos de escritura", LOG_DIR)
    sys.exit(1)

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
    ahora = datetime.now()
    nombre = ahora.strftime("%Y-%m-%d-%H") + ".log"
    ruta = os.path.join(LOG_DIR, nombre)
    with open(ruta, "a", encoding="utf-8") as f:
        f.write(f"[{ahora.strftime('%Y-%m-%d %H:%M:%S')}]\n{texto}\n---\n")

# -------------------------
# Workers (I/O en hilos separados — no bloquean la UI)
# -------------------------
class _IpPuertosWorker(QObject):
    resultado = pyqtSignal(str, str)

    def run(self):
        ip = "desactivado"
        if OBTENER_IP_PUBLICA:
            try:
                ip = red.obtener_ip_publica()
            except Exception:
                ip = "N/A"
        try:
            puertos_text = "\n".join(puertos.puertos_abiertos())
        except Exception:
            puertos_text = "N/A"
        self.resultado.emit(ip, puertos_text)


class _RedWorker(QObject):
    resultado = pyqtSignal(str)

    def run(self):
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
                vel_text += f"{iface}: ↓ {v.get('recibidos', '?')} ↑ {v.get('enviados', '?')}\n"
        self.resultado.emit(vel_text)


class _ProcServWorker(QObject):
    resultado = pyqtSignal(str, str)

    def run(self):
        try:
            top_proc = procesos.procesos_principales(3)
            proc_text = "\n".join([f"{name} ({cpu}%)" for _, name, cpu in top_proc])
        except Exception:
            proc_text = "N/A"
        try:
            serv_text = "\n".join([servicios.estado_servicio(s) for s in SERVICIOS])
        except Exception:
            serv_text = "N/A"
        self.resultado.emit(proc_text, serv_text)


class _SistemaWorker(QObject):
    resultado = pyqtSignal(str, str, str)

    def run(self):
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
        self.resultado.emit(temp, ram, disco)


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

        self.datos_ip_puertos = ""
        self.datos_red        = ""
        self.datos_proc_serv  = ""
        self.datos_sistema    = ""

        self._setup_workers()
        self._setup_timers()

    def _setup_workers(self):
        # Cada worker vive en su propio hilo — los timers disparan run() via señal
        self._thread_ip   = QThread()
        self._worker_ip   = _IpPuertosWorker()
        self._worker_ip.moveToThread(self._thread_ip)
        self._worker_ip.resultado.connect(self._on_ip_puertos)
        self._thread_ip.start()

        self._thread_red  = QThread()
        self._worker_red  = _RedWorker()
        self._worker_red.moveToThread(self._thread_red)
        self._worker_red.resultado.connect(self._on_red)
        self._thread_red.start()

        self._thread_proc = QThread()
        self._worker_proc = _ProcServWorker()
        self._worker_proc.moveToThread(self._thread_proc)
        self._worker_proc.resultado.connect(self._on_proc_serv)
        self._thread_proc.start()

        self._thread_sys  = QThread()
        self._worker_sys  = _SistemaWorker()
        self._worker_sys.moveToThread(self._thread_sys)
        self._worker_sys.resultado.connect(self._on_sistema)
        self._thread_sys.start()

    def _setup_timers(self):
        t = QTimer(self)
        t.timeout.connect(self._worker_ip.run)
        t.start(INTERVALO_IP_PUERTOS)

        t = QTimer(self)
        t.timeout.connect(self._worker_red.run)
        t.start(INTERVALO_RED)

        t = QTimer(self)
        t.timeout.connect(self._worker_proc.run)
        t.start(INTERVALO_PROC_SERV)

        t = QTimer(self)
        t.timeout.connect(self._worker_sys.run)
        t.start(INTERVALO_SISTEMA)

        # Limpieza de logs cada hora — no en cada escritura
        t = QTimer(self)
        t.timeout.connect(limpiar_logs)
        t.start(60 * 60 * 1000)

    def closeEvent(self, event):
        for thread in (self._thread_ip, self._thread_red,
                        self._thread_proc, self._thread_sys):
            thread.quit()
            thread.wait()
        super().closeEvent(event)

    def refrescar_widget(self):
        texto = (
            f"\n=== RaspKali Widget ===\n"
            f"{self.datos_ip_puertos}\n\n"
            f"{self.datos_red}\n"
            f"{self.datos_sistema}\n\n"
            f"{self.datos_proc_serv}\n"
        )
        self.label.setText(texto)

    def _on_ip_puertos(self, ip, puertos_text):
        self.datos_ip_puertos = f"IP Pública: {ip}\nPuertos abiertos:\n{puertos_text}"
        self.refrescar_widget()
        guardar_registro(self.datos_ip_puertos)

    def _on_red(self, vel_text):
        self.datos_red = f"Redes:\n{vel_text}"
        self.refrescar_widget()
        guardar_registro(self.datos_red)

    def _on_proc_serv(self, proc_text, serv_text):
        self.datos_proc_serv = f"Procesos:\n{proc_text}\n\nServicios:\n{serv_text}"
        self.refrescar_widget()
        guardar_registro(self.datos_proc_serv)

    def _on_sistema(self, temp, ram, disco):
        self.datos_sistema = f"Temp CPU: {temp}\nRAM: {ram}\nDisco: {disco}"
        self.refrescar_widget()
        guardar_registro(self.datos_sistema)


# -------------------------
# Main
# -------------------------
if __name__ == "__main__":
    _escribir_pid()
    atexit.register(_eliminar_pid)
    app = QApplication(sys.argv)

    def _salir(signum, _):
        log.info("Señal %s recibida — cerrando", signum)
        _eliminar_pid()
        app.quit()

    signal.signal(signal.SIGTERM, _salir)
    signal.signal(signal.SIGINT, _salir)

    ventana = RaspKaliWidget()
    ventana.show()
    sys.exit(app.exec_())
