import subprocess

def temperatura_cpu():
    try:
        salida = subprocess.check_output(["sensors"]).decode()
        for linea in salida.splitlines():
            if "temp1" in linea:
                return linea.split()[1]
        return "No detectada"
    except:
        return "No disponible"
