import tkinter as tk
import psutil, requests, os, subprocess

def obtener_ip_publica():
    try:
        return requests.get("https://ifconfig.me").text.strip()
    except:
        return "No disponible"

def obtener_temperatura():
    try:
        salida = subprocess.check_output(["sensors"]).decode()
        for linea in salida.splitlines():
            if "temp1" in linea:
                return linea.split()[1]
        return "No detectada"
    except:
        return "No disponible"

def actualizar_info():
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory()
    disco = psutil.disk_usage('/')
    ip = obtener_ip_publica()
    temp = obtener_temperatura()

    texto = f"""
    === RaspKali Monitor ===
    IP Pública: {ip}
    CPU: {cpu}% | Temp: {temp}
    RAM: {ram.percent}% ({ram.used//(1024**2)}MB / {ram.total//(1024**2)}MB)
    Disco: {disco.percent}% usado ({disco.used//(1024**3)}GB / {disco.total//(1024**3)}GB)
    """
    label.config(text=texto)
    root.after(3000, actualizar_info)

root = tk.Tk()
root.title("RaspKali Monitor")
label = tk.Label(root, font=("DejaVu Sans Mono", 10), justify="left")
label.pack()
actualizar_info()
root.mainloop()
