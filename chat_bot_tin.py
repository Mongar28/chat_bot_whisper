from transformers import pipeline, AutoModelForCausalLM, AutoModelForSpeechSeq2Seq, AutoProcessor
import torch
import telebot


def whisper4():
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

    assistant_model_id = "distil-whisper/distil-large-v2"

    assistant_model = AutoModelForCausalLM.from_pretrained(
        assistant_model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
    )
    assistant_model.to(device)

    model_id = "openai/whisper-large-v2"

    model = AutoModelForSpeechSeq2Seq.from_pretrained(
        model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
    )

    model.to(device)

    processor = AutoProcessor.from_pretrained(model_id)

    pipe = pipeline(
        "automatic-speech-recognition",
        model=model,
        tokenizer=processor.tokenizer,
        feature_extractor=processor.feature_extractor,
        max_new_tokens=128,
        chunk_length_s=30,
        batch_size=16,

        generate_kwargs={"assistant_model": assistant_model},
        torch_dtype=torch_dtype,
        device=device,
    )

    
    return pipe

pipe = whisper4()

# Mensaje de inicio

mensaje = """🤖𝘽𝙞𝙚𝙣𝙫𝙚𝙣𝙞𝙙𝙤𝙨 𝙖𝙡 𝘽𝙤𝙩 𝙙𝙚 𝙡𝙖 𝙡𝙞𝙣𝙚𝙖:🤖

🧠🐝*Ｔｅｒｒｉｔｏｒｉｏｓ Ｉｎｔｅｌｉｇｅｎｔｅｓ*🐝🧠​ \n\n\n"""

mensaje += """🎧⌨️✍Para transcribir solo debes hacer lo siguiente: mandar una nota o archvio de audio y tener en cuenta esto:\n\n
✅ El archivo de audio no puede pesar mas de 20 MG \n
✅ El Bot funcionará de mejor forma si la voz en el audio es clara y se entiende.\n
✅ Al final, el Bot devolvera un archivo word que contendrá el texto de las transcripción\n
✅ Entre más largo el audio, mayor será la espera en la respuesta \n"""

from pydub import AudioSegment

def convertir_a_mp3(archivo_audio_entrada, archivo_audio_salida):
    try:
        # Carga el archivo de audio de entrada
        audio = AudioSegment.from_file(archivo_audio_entrada)

        # Convierte el archivo de audio a MP3
        audio.export(archivo_audio_salida, format="mp3")

        print(f"Archivo de audio convertido a {archivo_audio_salida}")
    except Exception as e:
        print(f"Ocurrió un error durante la conversión: {str(e)}")
        
        


import docx
import datetime

def file_audio(message, pipe):
    # Si el audio es un archivo
    # Descarga delarchivo de audio
    nombre_audio = message.audio.file_name
    file_info = bot.get_file(message.audio.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    # Escritura del archivo de audio para luego pasarlo a wisper
    with open(f'audios/{nombre_audio}', 'wb') as new_file:
        new_file.write(downloaded_file)

    # pasamos el archivo de audio al modelo de wisper
    #pipe = whisper3()
    result = pipe(f'audios/{nombre_audio}', return_timestamps=True, generate_kwargs={"language": "spanish"})
    mensaje = result["text"]
    lon_mensaje = len(mensaje.split(" "))
        # Información sobre el audio
    meta_audio = f"""
    *- Nombre del archivo:*{message.audio.file_name}
    *- Tamaño:*{message.audio.file_size}
    *- Duración:*{message.audio.duration}
    *- Numero de palabras transcritas:{lon_mensaje}
    \n\n\n
    """
    #bot.send_message(message.chat.id, meta_audio, parse_mode = "Markdown")
    print(meta_audio)


    print(f"El texto que se transcriobió es el siguiente:\n\n{mensaje}")
    # escribimos el archivo .txt para enviarlo al usuario
    nombre_archivo = f'documentos/{nombre_audio}.docx'

    # Crea un nuevo documento
    doc = docx.Document()

    # Agrega un párrafo al documento
    doc.add_paragraph(f"Texto del audio transcrito:\n\n{mensaje}")

    # Guarda el documento en un archivo .docx
    doc.save(nombre_archivo)

    # Abrimos el archivo y lo enviamos
    file_txt = open(f'documentos/{nombre_audio}.docx', 'rb')


    # Creación del archivo txt que se guardará
    # nombre de usuario
    usuario = message.from_user.first_name
    # Creamos una variable fecha que contendrá el dia y la hora en la que se utilizó el bot
    fecha_hora_actual = datetime.datetime.now()
    fecha_hora = f"{fecha_hora_actual.strftime('%Y-%m-%d__%H:%M:%S')}"
    # Duracion del audio
    with open(f"documentos/{nombre_audio}.docx", "a", encoding="utf-8") as archivo:
        archivo.write(f"{usuario}___{fecha_hora_actual}___{mensaje}___{lon_mensaje}___{message.audio.file_size / 1000}___{message.audio.duration / 60}" + "\n")
        
    return file_txt,lon_mensaje

    
    
def file_voice(message, pipe):

  # Descarga delarchivo de audio
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    # Escritura del archivo de audio para luego pasarlo a wisper
    with open(f'audios/new_file.ogg', 'wb') as new_file:
        new_file.write(downloaded_file)

    # pasamos el archvio de audio al modelo de wisper
    #pipe = whisper3()
    result = pipe('audios/new_file.ogg', return_timestamps=True, generate_kwargs={"language": "spanish"})


    # enviamos el mensaje al usuario
    mensaje_t = result["text"]
    print(f"El texto que se transcriobió es el siguiente:\n\n{mensaje_t}")
    #mensaje = f"*El texto de la transcripción es es siguiente:*\n\n{mensaje_t}"

    #conteo de palabras transcritas
    conteo = len(mensaje_t.split(" "))

    # Creación del archivo txt que se guardará
    # nombre de usuario
    usuario = message.from_user.first_name
    # Creamos una variable fecha que contendrá el dia y la hora en la que se utilizó el bot
    fecha_hora_actual = datetime.datetime.now()
    fecha_hora = f"{fecha_hora_actual.strftime('%Y-%m-%d__%H:%M:%S')}"
    # Creamos un archivo txt
    with open("documentos/data_audios.txt", "a", encoding="utf-8") as archivo:
      archivo.write(f"{usuario}___{fecha_hora_actual}___{mensaje_t}___{conteo}___{message.voice.file_size / 1000}___{message.voice.duration / 60}" + "\n")


    return mensaje_t


from numpy.core.arrayprint import printoptions
bot = telebot.TeleBot('6575087955:AAH_05MzSh8hyw1L_wRCXVOLV97p6vK6Qew')

# Bot /start
@bot.message_handler(commands=['start', 'transcribir'])
def send_welcome(message):
    bot.reply_to(message, mensaje, parse_mode = "Markdown")

# Transcripción del audio y envio del archivo
@bot.message_handler(content_types=["text", "audio", "voice"],)
def bot_mensajes_texto(message):

  # Si el audio es un archivo
  if message.audio:

    mensaje_espera = f"""
    Tu audio se esta procesando y puede tardar un poco.\n\n🅣🅡🅐🅝🅢🅒🅡🅘🅑🅘🅔🅝🅓🅞...🎧⌨️⌛\n\n
    𝗡𝗼𝗺𝗯𝗿𝗲 𝗱𝗲𝗹 𝗮𝗿𝗰𝗵𝗶𝘃𝗼:{message.audio.file_name}
    𝗧𝗮𝗺𝗮𝗻̃𝗼:{message.audio.file_size} KB
    𝗗𝘂𝗿𝗮𝗰𝗶𝗼́𝗻:{message.audio.duration} Segundos.
    \n\n\n
    """

    user_name = message.from_user.first_name
    print(f"se esta procesando el audio de: {user_name}")
    bot.send_message(message.chat.id, mensaje_espera)

    # Abrimos el archivo y lo enviamos
    bot.send_chat_action(message.chat.id, "upload_document")

    file_txt, len_ = file_audio(message, pipe)
    # Enviar archivo
    bot.send_document(message.chat.id, file_txt, caption = f"𝗡𝘂𝗺𝗲𝗿𝗼 𝗱𝗲 𝗽𝗮𝗹𝗮𝗯𝗿𝗮𝘀 𝘁𝗿𝗮𝗻𝘀𝗰𝗿𝗶𝘁𝗮𝘀:{len_}")

  # Si el audio es un voice
  elif message.voice:

    mensaje_espera = f"""
    Tu audio se esta procesando y puede tardar un poco.\n\n🅣🅡🅐🅝🅢🅒🅡🅘🅑🅘🅔🅝🅓🅞...🎧⌨️⌛\n\n
    𝗡𝗼𝗺𝗯𝗿𝗲 𝗱𝗲𝗹 𝗮𝗿𝗰𝗵𝗶𝘃𝗼:{message.voice.file_name}
    𝗧𝗮𝗺𝗮𝗻̃𝗼:{message.voice.file_size} KB
    𝗗𝘂𝗿𝗮𝗰𝗶𝗼́𝗻:{message.voice.duration} Segundos.
    \n\n\n
    """

    user_name = message.from_user.first_name
    print(f"se esta procesando el audio de: {user_name}")

    bot.send_message(message.chat.id, mensaje_espera)
    print(mensaje_espera)
    mensaje = file_voice(message, pipe)
    len_mensaje = mensaje.split(" ")
    bot.send_message(message.chat.id, f"🅣🅡🅐🅝🅢🅒🅡🅘🅟🅒🅘🅞🅝: {mensaje} \n\n 𝗡𝘂𝗺𝗲𝗿𝗼 𝗱𝗲 𝗽𝗮𝗹𝗮𝗯𝗿𝗮𝘀 𝘁𝗿𝗮𝗻𝘀𝗰𝗿𝗶𝘁𝗮𝘀:{len(len_mensaje)}")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)



bot.infinity_polling()