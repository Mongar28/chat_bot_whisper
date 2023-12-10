FROM python:3.11-bullseye 

# Instalar FFmpeg
RUN apt-get update && apt-get install -y ffmpeg

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos necesarios al contenedor
COPY chat_bot_tin.py .
COPY requirements.txt .

# Instala las dependencias (si las hay)
RUN pip install --no-cache-dir -r requirements.txt

# Comando para ejecutar el script
CMD ["python", "chat_bot_tin.py"]