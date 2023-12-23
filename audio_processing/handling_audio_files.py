import telebot

# Funcion que se ejecuta en caso de que  el mensaje sea un arvhico de de audio
def file_audio(message, pipe, bot):
    # Si el audio es un archivo
    # Descarga el archivo de audio
    
    nombre_audio = message.audio.file_name
    file_info = bot.get_file(message.audio.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    audio_file_path = f'audios/{nombre_audio}'
    
    # Escritura del archivo de audio para luego pasarlo a wisper
    with open(audio_file_path, 'wb') as new_file:
        new_file.write(downloaded_file)

    # pasamos el archivo de audio al modelo de wisper
    result = pipe(audio_file_path, return_timestamps=True, generate_kwargs={"language": "spanish"})
    transcripcion = result["text"]
    numero_palabras = len(transcripcion.split(" "))\
    
    # Información sobre el audio
    meta_audio = f"""
- Nombre del archivo: {message.audio.file_name}
- Tamaño: {message.audio.file_size / 1048576:.2f} MG
- Duración: {message.audio.duration / 60:.2f} Minutos
- Numero de palabras transcritas: {numero_palabras}
    """
    
    return transcripcion, meta_audio, nombre_audio, numero_palabras


# Funcion que se ejecuta en caso de que  el mensake sea una nota de voz
def file_voice(message, pipe, bot):

  # Descarga delarchivo de audio
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    # Escritura del archivo de audio para luego pasarlo a wisper
    with open('new_file.ogg', 'wb') as new_file:
        new_file.write(downloaded_file)

    # pasamos el archvio de audio al modelo de wisper
    result = pipe('new_file.ogg', return_timestamps=True, generate_kwargs={"language": "spanish"})

    # enviamos el mensaje al usuario
    transcripcion = result["text"]

    #conteo de palabras transcritas
    conteo = len(transcripcion.split(" "))


    return transcripcion