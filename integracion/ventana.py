import tkinter as tk
import os, glob, sys
from datetime import datetime, timedelta
import configparser
from utils import red, memoria, temperatura, procesos, servicios, puertos

# === Leer archivo de configuración ===
config = configparser.ConfigParser()
if not config.read("config.ini"):
    print("Error: No se encontró el archivo config.ini")
    sys.exit(1)

# Validar valores
def validar_config():
    # Retención
    retencion = config.get("logs", "retencion", fallback=None)
    if retencion not in ["dia", "semana", "mes"]:
        print("Error en config.ini: 'retencion' debe ser 'dia', 'semana' o 'mes'")
        sys.exit(1)

    # Intervalos
    for clave in ["intervalo_ip_puertos", "intervalo_red", "intervalo_proc_serv", "intervalo_sistema"]:
        try:
            valor = config.getint("widget", clave)
            if valor <= 0:
                raise ValueError
        except:
            print(f"Error en config.ini: '{clave}' debe ser un número entero positivo (segundos)")
            sys.exit(1)

    # Transparencia
    try:
        trans = config.getfloat("widget", "transparencia")
        if not (0.0 <= trans <= 1.0):
            raise ValueError
    except:
        print("Error en config.ini: 'transparencia' debe estar entre 0.0 y 1.0")
        sys.exit(1)

validar_config()

# === Configuración del widget ===
RETENCION = config.get("logs", "retencion")
POS_X = config.getint("widget", "posicion_x")
POS_Y = config.getint("widget", "posicion_y")
FUENTE = config.get("widget", "fuente")
TAMANO = config.getint("widget", "tamano_fuente")
COLOR_TEXTO = config.get("widget", "color_texto")
COLOR_FONDO = config.get("widget", "color_fondo")
TRANSPARENCIA = config.getfloat("widget", "transparencia")
ALINEACION = config.get("widget", "alineacion", fallback="left")

# Intervalos (convertidos a ms)
INTERVALO_IP_PUERTOS = config.getint("widget", "intervalo_ip_puertos") * 1000
INTERVALO_RED = config.getint("widget", "intervalo_red") * 1000
INTERVALO_PROC_SERV = config.getint("widget", "intervalo_proc_serv") * 1000
INTERVALO_SISTEMA = config.getint("widget", "intervalo_sistema") * 1000

# === Configuración de logs ===
LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

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
        except:
            pass

def guardar_registro(texto):
    nombre = datetime.now().strftime("%Y-%m-%d-%H") + ".log"
    ruta = os.path.join(LOG_DIR, nombre)
    with open(ruta, "a") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]\n{texto}\n---\n")
    limpiar_logs()

# === Variables globales ===
datos_ip_puertos = ""
datos_red = ""
datos_proc_serv = ""
datos_sistema = ""

# === Funciones de actualización ===
def actualizar_ip_puertos():
    global datos_ip_puertos
    ip = red.obtener_ip_publica()
    puertos_text = "\n".join(puertos.puertos_abiertos())
    datos_ip_puertos = f"IP Pública: {ip}\nPuertos abiertos:\n{puertos_text}"
    refrescar_widget()
    guardar_registro(datos_ip_puertos)
    root.after(INTERVALO_IP_PUERTOS, actualizar_ip_puertos)

def actualizar_red():
    global datos_red
    interfaces = red.listar_interfaces()
    velocidades = red.velocidad_por_interfaz()
    vel_text = ""
    for iface in interfaces:
        if iface in velocidades:
            v = velocidades[iface]
            vel_text += f"{iface}: ↓ {v['recibidos']} ↑ {v['enviados']}\n"
    datos_red = f"Redes:\n{vel_text}"
    refrescar_widget()
    guardar_registro(datos_red)
    root.after(INTERVALO_RED, actualizar_red)

def actualizar_proc_serv():
    global datos_proc_serv
    top_proc = procesos.procesos_principales(3)
    proc_text = "\n".join([f"{name} ({cpu}%)" for _, name, cpu in top_proc])
    servicios_list = ["ssh", "apache2", "mysql"]
    serv_text = "\n".join([servicios.estado_servicio(s) for s in servicios_list])
    datos_proc_serv = f"Procesos:\n{proc_text}\n\nServicios:\n{serv_text}"
    refrescar_widget()
    guardar_registro(datos_proc_serv)
    root.after(INTERVALO_PROC_SERV, actualizar_proc_serv)

def actualizar_sistema():
    global datos_sistema
    temp = temperatura.temperatura_cpu()
    ram = memoria.memoria_ram()
    disco = memoria.almacenamiento()
    datos_sistema = f"Temp CPU: {temp}\nRAM: {ram}\nDisco: {disco}"
    refrescar_widget()
    guardar_registro(datos_sistema)
    root.after(INTERVALO_SISTEMA, actualizar_sistema)

def refrescar_widget():
    texto = f"""
    === RaspKali Widget ===
    {datos_ip_puertos}

    {datos_red}

    {datos_sistema}

    {datos_proc_serv}
    """
    label.config(text=texto)

# === Ventana estilo widget ===
root = tk.Tk()
root.overrideredirect(True)
root.attributes("-topmost", True)
root.geometry(f"+{POS_X}+{POS_Y}")
root.configure(bg=COLOR_FONDO)
root.attributes("-alpha", TRANSPARENCIA)

label = tk.Label(root, font=(FUENTE, TAMANO), fg=COLOR_TEXTO, bg=COLOR_FONDO,
                 justify=ALINEACION, anchor="w")
label.pack(padx=10, pady=10)

# === Iniciar actualizaciones ===
actualizar_ip_puertos()
actualizar_red()
actualizar_proc_serv()
actualizar_sistema()

root.mainloop()
