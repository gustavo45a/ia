from gtts import gTTS
import os

def generar_tts(texto, nombre="respuesta.mp3"):
    tts = gTTS(texto, lang="es")
    tts.save(nombre)
    return nombre
