import requests, psutil

def obtener_ip_publica():
    try:
        return requests.get("https://ifconfig.me").text.strip()
    except:
        return "No disponible"

def velocidad_red(interface="eth0"):
    net_io = psutil.net_io_counters(pernic=True)
    if interface in net_io:
        datos = net_io[interface]
        return f"Enviados: {datos.bytes_sent} | Recibidos: {datos.bytes_recv}"
    return "Interfaz no encontrada"
