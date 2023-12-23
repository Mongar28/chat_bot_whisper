
# función que retorna el mensaje de bienvenida
def mensaje_bienvenida():
    mensaje_de_bienvenida = """🤖𝘽𝙞𝙚𝙣𝙫𝙚𝙣𝙞𝙙𝙤𝙨 𝙖𝙡 𝘽𝙤𝙩 𝙙𝙚 𝙡𝙖 𝙡𝙞𝙣𝙚𝙖🤖
    🧠🐝*Ｔｅｒｒｉｔｏｒｉｏｓ Ｉｎｔｅｌｉｇｅｎｔｅｓ*🐝🧠​ 

    🎧⌨️✍Para transcribir solo debes hacer lo siguiente: mandar una nota o archvio de audio y tener en cuenta esto:\n
    ✅ El archivo de audio no puede pesar mas de 20 MG 
    ✅ El Bot funcionará de mejor forma si la voz en el audio es clara y se entiende.
    ✅ Al final, el Bot devolvera un archivo word que contendrá el texto de las transcripción.
    ✅ Entre más largo el audio, mayor será la espera en la respuesta. \n"""

    return mensaje_de_bienvenida

# Funcion que retorna el mensaje de espera
def mensaje_de_espera(message):
    audio_name = ''
    audio_size = ''
    audio_duration = ''
  
    if message.audio:
        audio_name = message.audio.file_name
        audio_size = message.audio.file_size
        audio_duration = message.audio.duration
    else: 
        audio_name = f"nota_de_voz_de_{message.from_user.first_name}"
        audio_size = message.voice.file_size
        audio_duration = message.voice.duration

    mensaje_espera = f"""
    Tu audio se esta procesando y puede tardar un poco.\n\n🅣🅡🅐🅝🅢🅒🅡🅘🅑🅘🅔🅝🅓🅞...🎧⌨️⌛\n\n
    𝗡𝗼𝗺𝗯𝗿𝗲 𝗱𝗲𝗹 𝗮𝗿𝗰𝗵𝗶𝘃𝗼: {audio_name}
    𝗧𝗮𝗺𝗮𝗻̃𝗼: {audio_size / 1048576:.2f} MG
    𝗗𝘂𝗿𝗮𝗰𝗶𝗼́𝗻: {audio_duration / 60:.2f} Minutos.
    \n\n\n
    """
    
    return mensaje_espera