import psutil

def puertos_abiertos():
    try:
        conexiones = psutil.net_connections(kind='inet')
    except psutil.AccessDenied:
        return ["Sin permiso"]
    abiertos = []
    for c in conexiones:
        if c.status == 'LISTEN':
            abiertos.append(f"Puerto {c.laddr.port} ({c.type})")
    return abiertos if abiertos else ["Ninguno"]
