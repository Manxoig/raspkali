import psutil

def puertos_abiertos():
    conexiones = psutil.net_connections(kind='inet')
    abiertos = []
    for c in conexiones:
        if c.status == 'LISTEN':
            abiertos.append(f"Puerto {c.laddr.port} ({c.type})")
    return abiertos if abiertos else ["Ninguno"]
