# Dockerfile para probar RaspKali Widget en contenedor
FROM python:3.9-slim

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    lm-sensors \
    procps \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependencias Python
RUN pip install --no-cache-dir \
    psutil \
    requests \
    PyQt5 \
    unittest

# Copiar el proyecto
WORKDIR /app
COPY . .

# Hacer ejecutable el script de tests
RUN chmod +x run_tests.py

# Comando por defecto: ejecutar tests
CMD ["python3", "run_tests.py"]
