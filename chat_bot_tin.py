import telebot
from decouple import config
from audio_processing.whisper import whisper3
from chat_bot.chat_behavior import mensaje_bienvenida, mensaje_de_espera
from audio_processing.handling_audio_files import file_audio, file_voice
from audio_processing.create_docx import docx_generator 


# cargamos el modelo whisper
pipe = whisper3()

# instanciamos la clase telebot.TeleBot
token = config('api_token')
bot = telebot.TeleBot(token)

# Mensaje de inicio
mensaje_bienvenida = mensaje_bienvenida()

# Bot /start
@bot.message_handler(commands=['start', 'transcribir'])
def send_welcome(message):
    bot.reply_to(message, mensaje_bienvenida, parse_mode = "Markdown")
    
# Transcripción del audio y envio del archivo
@bot.message_handler(content_types=["text", "audio", "voice"],)
def bot_mensajes_texto(message):
  
  mensaje_espera = mensaje_de_espera(message)

  # Si el audio es un archivo
  if message.audio:
    user_name = message.from_user.first_name
    print(f"se esta procesando el audio de: {user_name}")
    bot.send_message(message.chat.id, mensaje_espera)

    # Abrimos el archivo y lo enviamos
    bot.send_chat_action(message.chat.id, "upload_document")

    # Ejecutamos la función file_audio la cual importa y procesa el audio
    transcripcion, meta_audio, nombre_audio, numero_palabras = file_audio(message, pipe, bot)

    # Generamos el archvio con la transcripcion
    file_txt = docx_generator(message, transcripcion, nombre_audio, meta_audio)
    
    # Enviar archivo
    bot.send_document(message.chat.id, file_txt, caption = f"𝗡𝘂𝗺𝗲𝗿𝗼 𝗱𝗲 𝗽𝗮𝗹𝗮𝗯𝗿𝗮𝘀 𝘁𝗿𝗮𝗻𝘀𝗰𝗿𝗶𝘁𝗮𝘀:{numero_palabras}")

  # Si el audio es un voice
  elif message.voice:

    user_name = message.from_user.first_name
    print(f"se esta procesando el audio de: {user_name}")

    bot.send_message(message.chat.id, mensaje_espera)
    print(mensaje_espera)
    transcripcion = file_voice(message, pipe, bot)
    len_mensaje = transcripcion.split(" ")
    bot.send_message(message.chat.id, f"🅣🅡🅐🅝🅢🅒🅡🅘🅟🅒🅘🅞🅝: {transcripcion} \n\n 𝗡𝘂𝗺𝗲𝗿𝗼 𝗱𝗲 𝗽𝗮𝗹𝗮𝗯𝗿𝗮𝘀 𝘁𝗿𝗮𝗻𝘀𝗰𝗿𝗶𝘁𝗮𝘀:{len(len_mensaje)}")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)



bot.infinity_polling()