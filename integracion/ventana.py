import tkinter as tk
from utils import red, memoria, temperatura, procesos, servicios

def actualizar_info():
    # Datos básicos
    ip = red.obtener_ip_publica()
    temp = temperatura.temperatura_cpu()
    ram = memoria.memoria_ram()
    disco = memoria.almacenamiento()
    vel_red = red.velocidad_red("eth0")

    # Procesos principales
    top_proc = procesos.procesos_principales(5)
    proc_text = "\n".join([f"PID {pid} {name} - {cpu}%" for pid, name, cpu in top_proc])

    # Estado de servicios críticos
    servicios_list = ["ssh", "apache2", "mysql"]
    serv_text = "\n".join([servicios.estado_servicio(s) for s in servicios_list])

    # Texto final
    texto = f"""
    === RaspKali Monitor ===
    IP Pública: {ip}
    CPU Temp: {temp}
    RAM: {ram}
    Disco: {disco}
    Red (eth0): {vel_red}

    --- Procesos principales ---
    {proc_text}

    --- Servicios ---
    {serv_text}
    """

    label.config(text=texto)
    root.after(5000, actualizar_info)  # refresca cada 5 segundos

# Ventana principal
root = tk.Tk()
root.title("RaspKali Monitor")
label = tk.Label(root, font=("DejaVu Sans Mono", 10), justify="left", anchor="w")
label.pack(padx=10, pady=10)

# Inicia actualización
actualizar_info()
root.mainloop()
