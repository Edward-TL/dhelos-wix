# Usa una imagen base oficial de Python.
# Es recomendable usar una imagen que coincida con la versión de Python que quieres usar
# y que esté optimizada para funciones (como las 'buster' o 'slim').
# Consulta la documentación de Google Cloud Functions para ver las imágenes soportadas.
# python:3.11-buster es una buena opción para Python 3.11.
FROM python:3.13-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /dhelos-wix

RUN apt-get update && \
    apt-get install -y --no-install-recommends git && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

# Copia el archivo de requerimientos primero.
# Esto permite a Docker usar el cache si los requerimientos no han cambiado,
# acelerando las futuras builds.
COPY requirements.txt .

# Instala las dependencias.
# El flag --no-cache-dir evita almacenar la cache de pip, lo que reduce el tamaño de la imagen.
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el código restante del proyecto (tu main.py, etc.) al directorio de trabajo.
# Esto debe hacerse después de instalar dependencias para aprovechar el cache.
COPY . .

# 'process_sheet_row' es el nombre de la función Python que quieres ejecutar
# cuando se reciba una petición HTTP.
ENV FUNCTION_TARGET=load_to_drive

ENV PYTHONUNBUFFERED=1
ENV PORT=8080

# El comando por defecto que se ejecutará cuando el contenedor se inicie.
# `functions-framework` es la herramienta recomendada por Google para ejecutar
# funciones en contenedores localmente y en Cloud Run/Cloud Functions (2ª generación).
# La flag --target especifica el nombre de la función a ejecutar (lee de FUNCTION_TARGET).
# La flag --port es donde el framework escuchará las peticiones HTTP.

# Cloud Functions en contenedores siempre esperan que la función escuche en el puerto 8080.
# CMD ["gcloud", "functions", "deploy", "appointments",  "--trigger-http", "--allow-unauthenticated", "--port", "8080"]
CMD ["functions-framework", "--target", "load_to_drive", "--port", "8080"]

# Opcional: Exponer el puerto para desarrollo local, aunque Cloud Functions no lo necesita
# al desplegar, es útil para testear el contenedor con `docker run -p 8080:8080 ...`
# EXPOSE 8080