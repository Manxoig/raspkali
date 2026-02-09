import psutil

def memoria_ram():
    ram = psutil.virtual_memory()
    return f"{ram.percent}% ({ram.used//(1024**2)}MB / {ram.total//(1024**2)}MB)"

def almacenamiento():
    disco = psutil.disk_usage('/')
    return f"{disco.percent}% usado ({disco.used//(1024**3)}GB / {disco.total//(1024**3)}GB)"
