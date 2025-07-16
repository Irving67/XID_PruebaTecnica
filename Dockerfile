    # Usamos una versión oficial y estable de Python
    FROM python:3.11-slim-buster

    # Seteamos el directorio de trabajo dentro del contenedor
    WORKDIR /app

    # Instalar spaCy
    RUN pip install spacy

    # Descargar el modelo core en Español
    RUN python -m spacy download es_core_news_md

    # Copiar en la ruta de la aplicación
    COPY . /app

    # Instalamos las dependencias necesarias
    COPY requirements.txt .
    RUN pip install -r requirements.txt

    # Los certificados se piden para conexiones SSL, aquí se actualizan
    RUN apt-get install -y --no-install-recommends ca-certificates
    RUN update-ca-certificates

    # Copiamos todo el código de la aplicación
    COPY . .

    # Desplegamos en el puerto 8000 (Por convención)
    EXPOSE 8000

    # Comandos para ejecutar la aplicación de Flask
    CMD ["python", "app.py"]