import subprocess

def estado_servicio(servicio):
    try:
        salida = subprocess.check_output(["systemctl","is-active",servicio], timeout=5).decode().strip()
        return f"{servicio}: {salida}"
    except (subprocess.CalledProcessError, FileNotFoundError, OSError, subprocess.TimeoutExpired):
        return f"{servicio}: No disponible"
