import psutil


def procesos_principales(n=5):
    resultado = []
    for p in psutil.process_iter(["pid", "name", "cpu_percent"]):
        try:
            resultado.append((p.info["pid"], p.info["name"], p.info["cpu_percent"]))
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return sorted(resultado, key=lambda x: x[2], reverse=True)[:n]
