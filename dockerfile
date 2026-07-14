FROM python:3.10-slim

# Instalar Java 21 (requerido para PySpark en la nueva versión de Debian) y dependencias básicas
RUN mkdir -p /usr/share/man/man1 && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
    openjdk-21-jre-headless \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Configurar variable de entorno para apuntar a Java 21
ENV JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64

# Directorio de trabajo dentro del contenedor
WORKDIR /project

# Copiar e instalar las dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Mantener el contenedor encendido
CMD ["tail", "-f", "/dev/null"]