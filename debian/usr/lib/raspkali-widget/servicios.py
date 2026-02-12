import subprocess

def estado_servicio(servicio):
    try:
        salida = subprocess.check_output(["systemctl","is-active",servicio]).decode().strip()
        return f"{servicio}: {salida}"
    except:
        return f"{servicio}: No disponible"
