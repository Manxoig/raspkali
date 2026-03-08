import psutil, requests

def obtener_ip_publica():
    try:
        return requests.get("https://ifconfig.me").text.strip()
    except:
        return "No disponible"

def listar_interfaces():
    return list(psutil.net_if_addrs().keys())

def velocidad_por_interfaz():
    net_io = psutil.net_io_counters(pernic=True)
    datos = {}
    for iface, stats in net_io.items():
        datos[iface] = {
            "enviados": stats.bytes_sent,
            "recibidos": stats.bytes_recv
        }
    return datos
