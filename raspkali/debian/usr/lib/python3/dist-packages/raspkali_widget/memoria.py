import psutil

def memoria_ram():
    try:
        ram = psutil.virtual_memory()
        return f"{ram.percent}% ({ram.used//(1024**2)}MB / {ram.total//(1024**2)}MB)"
    except Exception:
        return "No disponible"

def almacenamiento():
    try:
        disco = psutil.disk_usage('/')
        return f"{disco.percent}% usado ({disco.used//(1024**3)}GB / {disco.total//(1024**3)}GB)"
    except OSError:
        return "No disponible"
