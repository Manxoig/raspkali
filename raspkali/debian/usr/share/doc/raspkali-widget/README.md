# RaspKali Widget Monitor

Widget flotante para monitorizar en tiempo real CPU, RAM, disco, red y servicios en Raspberry Pi con Kali/Ubuntu/Debian. Implementado en PyQt5 y distribuido como paquete `.deb`.

## Instalación

```
sudo dpkg -i raspkali-widget.deb
sudo apt-get install -f
```

## Construcción del paquete

```
sudo apt install dpkg-dev fakeroot build-essential lintian -y
fakeroot dpkg-deb --build debian/ raspkali-widget.deb
lintian raspkali-widget.deb
```

## Estructura instalada

```
/usr/bin/raspkali-widget          Ejecutable principal
/usr/bin/raspkali-widget-ctl      Script de control (start/stop/restart/status)
/usr/lib/python3/dist-packages/raspkali_widget/   Módulos Python
/etc/raspkali-widget/config.ini   Configuración
/var/log/raspkali-widget/         Directorio de logs (root:adm, 750)
/etc/xdg/autostart/raspkali-widget.desktop   Autoarranque de sesión
```

## Configuración (`/etc/raspkali-widget/config.ini`)

### [logs]
- `retencion`: tiempo de retención de logs — `dia`, `semana` (defecto), `mes`

### [widget]
- `posicion_x`, `posicion_y`: coordenadas de la ventana en pantalla
- `fuente`: nombre de la fuente (ej. `DejaVu Sans Mono`)
- `tamano_fuente`: tamaño en puntos
- `color_texto`, `color_fondo`: colores en formato `#RRGGBB`
- `transparencia`: opacidad entre `0.0` y `1.0`
- `alineacion`: `left`, `center` o `right`
- `servicios`: lista separada por comas de servicios a monitorizar (ej. `ssh,apache2`)
- `obtener_ip_publica`: `true` / `false` (ver sección Privacidad)
- `intervalo_ip_puertos`: segundos entre actualizaciones de IP y puertos
- `intervalo_red`: segundos entre actualizaciones de velocidad de red
- `intervalo_proc_serv`: segundos entre actualizaciones de procesos y servicios
- `intervalo_sistema`: segundos entre actualizaciones de CPU, RAM y disco

## Privacidad y datos de red

La consulta de IP pública a `https://ifconfig.me` está **desactivada por defecto**.
Para activarla, editar `/etc/raspkali-widget/config.ini`:

```ini
[widget]
obtener_ip_publica = true
```

Con esta opción activa, el sistema envía periódicamente una solicitud HTTP a `ifconfig.me`.
Si no necesitas visualizar tu IP pública, mantén el valor en `false`.

## Control del servicio

```
raspkali-widget-ctl start
raspkali-widget-ctl stop
raspkali-widget-ctl restart
raspkali-widget-ctl status
```

El script requiere una sesión de escritorio con `XDG_RUNTIME_DIR` definido.

## Logs

Los logs se escriben en `/var/log/raspkali-widget/` (accesible a `root` y miembros del grupo `adm`).
La retención se configura con el parámetro `retencion` en `config.ini`.
