# Documentación de la API - RaspKali Widget

Esta documentación describe los módulos y funciones del paquete `raspkali_widget`, utilizado por el RaspKali Widget para monitorear el sistema en tiempo real.

## Módulo `memoria`

Proporciona funciones para obtener información sobre la memoria RAM y el almacenamiento en disco.

### `memoria_ram()`
- **Descripción**: Obtiene el porcentaje de uso de la memoria RAM y los valores absolutos en MB.
- **Retorno**: Cadena de texto en formato `"X% (YMB / ZMB)"`.
- **Dependencias**: `psutil`.

### `almacenamiento()`
- **Descripción**: Obtiene el porcentaje de uso del disco raíz y los valores absolutos en GB.
- **Retorno**: Cadena de texto en formato `"X% usado (YGB / ZGB)"`.
- **Dependencias**: `psutil`.

## Módulo `procesos`

Maneja la información de procesos del sistema.

### `procesos_principales(n=5)`
- **Descripción**: Devuelve los `n` procesos con mayor uso de CPU.
- **Parámetros**:
  - `n` (int): Número de procesos a retornar (por defecto 5).
- **Retorno**: Lista de tuplas `[(pid, nombre, porcentaje_cpu), ...]`.
- **Dependencias**: `psutil`.

## Módulo `puertos`

Gestiona la información de puertos de red abiertos.

### `puertos_abiertos()`
- **Descripción**: Lista los puertos TCP/UDP en estado LISTEN.
- **Retorno**: Lista de cadenas `["Puerto X (tipo)", ...]` o `["Ninguno"]` si no hay.
- **Dependencias**: `psutil`.

## Módulo `red`

Proporciona datos sobre la red y conectividad.

### `obtener_ip_publica()`
- **Descripción**: Obtiene la dirección IP pública del dispositivo consultando un servicio externo.
- **Retorno**: Cadena con la IP o `"No disponible"` en caso de error.
- **Dependencias**: `requests`.

### `listar_interfaces()`
- **Descripción**: Lista los nombres de las interfaces de red disponibles.
- **Retorno**: Lista de cadenas con nombres de interfaces.
- **Dependencias**: `psutil`.

### `velocidad_por_interfaz()`
- **Descripción**: Obtiene la velocidad de red en bytes/segundo por interfaz. La primera llamada inicializa el estado; las siguientes retornan valores formateados.
- **Retorno**: Diccionario `{"interfaz": {"enviados": str, "recibidos": str}, ...}` (ej. `"1.5 KB/s"`). La primera llamada retorna `"..."` mientras se toman las mediciones iniciales.
- **Dependencias**: `psutil`.

## Módulo `servicios`

Verifica el estado de servicios del sistema.

### `estado_servicio(servicio)`
- **Descripción**: Consulta el estado de un servicio usando `systemctl`.
- **Parámetros**:
  - `servicio` (str): Nombre del servicio (ej. "ssh").
- **Retorno**: Cadena en formato `"servicio: estado"` o `"servicio: No disponible"`.
- **Dependencias**: `subprocess`, `systemctl`.

## Módulo `temperatura`

Obtiene la temperatura del CPU.

### `temperatura_cpu()`
- **Descripción**: Lee la temperatura del sensor usando el comando `sensors`.
- **Retorno**: Cadena con la temperatura (ej. "+45.0°C") o `"No detectada"`/`"No disponible"`.
- **Dependencias**: `subprocess`, `lm-sensors`.

## Configuración

El widget se configura mediante `config.ini` en `/etc/raspkali-widget/`. Ver el README para detalles de parámetros.

## Dependencias del Sistema

- Python 3
- psutil
- requests
- PyQt5
- lm-sensors (para temperatura)
- requests (para IP pública, opcional — desactivado por defecto)

## Uso en el Código Principal

El ejecutable `/usr/bin/raspkali-widget` importa estos módulos y actualiza la interfaz en hilos separados (QThread) según los intervalos definidos en `config.ini`. Los datos se muestran en una ventana flotante sin bordes, con transparencia y colores configurables.

## Tests

Se incluyen tests unitarios para verificar la funcionalidad de cada módulo. Los tests usan `unittest` y mocks para simular llamadas al sistema.

Para ejecutar los tests en un sistema Linux con las dependencias instaladas:
```
python3 run_tests.py
```

Los tests cubren:
- Retornos de tipos correctos.
- Manejo de errores (excepciones).
- Formatos de salida esperados.
- Mocks para llamadas externas (subprocess, requests).
- **Tests de lógica sin UI**: `test_ventana_logic.py` valida los métodos de actualización en `ventana.py` sin crear la interfaz gráfica.
- **Test general**: `test_general.py` verifica importaciones y existencia de funciones clave.