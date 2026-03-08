import psutil

def procesos_principales(n=5):
    procesos = [(p.info["pid"], p.info["name"], p.info["cpu_percent"])
                for p in psutil.process_iter(["pid","name","cpu_percent"])]
    procesos = sorted(procesos, key=lambda x: x[2], reverse=True)[:n]
    return procesos
