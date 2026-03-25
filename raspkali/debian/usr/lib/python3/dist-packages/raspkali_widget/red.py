import time
import psutil
import requests

_prev_counters = {}
_prev_time = None


def _formatear_bytes(bps):
    if bps < 1024:
        return f"{bps:.0f} B/s"
    elif bps < 1024 ** 2:
        return f"{bps / 1024:.1f} KB/s"
    return f"{bps / 1024 ** 2:.1f} MB/s"


def obtener_ip_publica():
    try:
        return requests.get("https://ifconfig.me", timeout=5).text.strip()
    except (requests.exceptions.RequestException, OSError):
        return "No disponible"


def listar_interfaces():
    return list(psutil.net_if_addrs().keys())


def velocidad_por_interfaz():
    global _prev_counters, _prev_time

    ahora = time.monotonic()
    curr = psutil.net_io_counters(pernic=True)

    if not _prev_counters or _prev_time is None:
        _prev_counters = curr
        _prev_time = ahora
        return {iface: {"enviados": "...", "recibidos": "..."} for iface in curr}

    elapsed = ahora - _prev_time
    datos = {}
    for iface, stats in curr.items():
        if iface in _prev_counters and elapsed > 0:
            prev = _prev_counters[iface]
            datos[iface] = {
                "enviados":   _formatear_bytes((stats.bytes_sent - prev.bytes_sent) / elapsed),
                "recibidos":  _formatear_bytes((stats.bytes_recv - prev.bytes_recv) / elapsed),
            }

    _prev_counters = curr
    _prev_time = ahora
    return datos
