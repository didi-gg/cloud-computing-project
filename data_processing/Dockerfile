# Imagen base de Python 3.9-slim
FROM python:3.9-slim

# Instalar cron
RUN apt-get update && apt-get install -y cron

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar el archivo requirements.txt
COPY requirements.txt .

# Instalar las dependencias desde requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY . .

# Copiar el archivo de cron jobs
COPY cronjob /etc/cron.d/cronjob

# Dar permisos de ejecución al archivo cronjob
RUN chmod 0644 /etc/cron.d/cronjob

# Aplicar los cron jobs
RUN crontab /etc/cron.d/cronjob

# Crear el log file para cron
RUN touch /var/log/cron.log

# Ejecutar cron en el contenedor
CMD cron && tail -f /var/log/cron.log