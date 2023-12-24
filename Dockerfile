# Usa una imagen de Python oficial como base
FROM python:3.11-bullseye 

# Instalar FFmpeg
RUN apt-get update && apt-get install -y ffmpeg

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el archivo requirements.txt al contenedor
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de la aplicación al contenedor
COPY . .



# Ejecuta tu aplicación cuando se inicie el contenedor
CMD ["python3", "chat_bot_tin.py"]






#FROM python:3.11-bullseye 

# Instalar FFmpeg
#RUN apt-get update && apt-get install -y ffmpeg

#USER root
#RUN apt-get update

#COPY ./run.sh /opt
#COPY ./requirements.txt /opt

#CMD ["/bin/bash","/opt/run.sh"]