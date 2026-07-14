FROM python:3.10-slim

# Instalar Java (requerido para PySpark) y dependencias básicas de compilación
RUN mkdir -p /usr/share/man/man1 && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
    openjdk-17-jre-headless \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Configurar variable de entorno para que Spark encuentre Java
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64

# Directorio de trabajo dentro del contenedor
WORKDIR /project

# Copiar e instalar las dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Mantener el contenedor encendido para poder entrar e interactuar con la terminal
CMD ["tail", "-f", "/dev/null"]