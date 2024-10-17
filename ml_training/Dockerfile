# Imagen base de Python 3.9-slim
FROM python:3.9-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar el archivo requirements.txt
COPY requirements.txt .

# Instalar las dependencias desde requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY . .

# Crear el log file para cron
RUN touch /var/log/cron.log

# Comando por defecto para ejecutar el script
CMD ["sleep", "infinity"]
