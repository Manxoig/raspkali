import subprocess

def temperatura_cpu():
    try:
        salida = subprocess.check_output(["sensors"], timeout=5).decode()
        for linea in salida.splitlines():
            if "temp1" in linea:
                return linea.split()[1]
        return "No detectada"
    except (subprocess.CalledProcessError, FileNotFoundError, OSError, subprocess.TimeoutExpired):
        return "No disponible"
