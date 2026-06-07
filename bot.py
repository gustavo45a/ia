import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
load_dotenv()

from config import elegir_modelo
from ia_fast import call_groq
from ia_pro import call_openrouter
from estado import actualizar_emocion, actualizar_tts, actualizar_conversacion, cargar_estado
from tts import generar_tts

def cargar_personalidad():
    with open("personality.txt", "r", encoding="utf-8") as f:
        return f.read()

PERSONALIDAD = cargar_personalidad()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# -----------------------------------
# EVENTO DE INICIO
# -----------------------------------
@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")

# -----------------------------------
# COMANDO PARA APAGAR EL BOT
# -----------------------------------
@bot.command()
async def off(ctx):
    await ctx.send("Apagando el bot... ¡Hasta luego!")
    await bot.close()

# -----------------------------------
# COMANDO PARA PRENDER EL BOT
# (Realmente solo responde, el bot ya está encendido)
# -----------------------------------
@bot.command()
async def on(ctx):
    await ctx.send("¡Ya estoy encendido y listo para ayudarte!")

# -----------------------------------
# ENTRAR A UN CANAL DE VOZ POR COMANDO HABLADO
# -----------------------------------
async def entrar_a_voz_por_texto(message):
    texto = message.content.lower()

    if "metete al chat de voz" in texto or "métete al chat de voz" in texto:
        # Extraer nombre del canal
        partes = texto.split("voz")
        if len(partes) < 2:
            await message.channel.send("Dime el nombre del canal de voz.")
            return

        nombre_canal = partes[1].strip()

        # Buscar canal
        canal = discord.utils.get(message.guild.voice_channels, name=nombre_canal)

        if canal is None:
            await message.channel.send(f"No encontré el canal de voz **{nombre_canal}**.")
            return

        # Conectar
        try:
            await canal.connect()
            await message.channel.send(f"Ya me metí al canal de voz **{nombre_canal}**.")
        except:
            await message.channel.send("No pude entrar al canal de voz.")
        return True

    return False

# -----------------------------------
# GENERAR PROMPT
# -----------------------------------
def generar_prompt(texto, emocion):
    return f"{PERSONALIDAD}\nEmoción actual: {emocion}\n\nUsuario: {texto}"

# -----------------------------------
# RESPONDER MENSAJES
# -----------------------------------
async def responder(texto):
    emocion = actualizar_emocion(texto)
    actualizar_tts(texto)
    actualizar_conversacion(texto)

    estado = cargar_estado()
    prompt = generar_prompt(texto, emocion)

    modo = elegir_modelo(texto)

    if modo == "fast":
        try:
            return call_groq(prompt)
        except:
            return call_openrouter(prompt)
    else:
        try:
            return call_openrouter(prompt)
        except:
            return call_groq(prompt)

# -----------------------------------
# EVENTO PRINCIPAL DE MENSAJES
# -----------------------------------
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # Primero: detectar si pidió entrar a un canal de voz
    if await entrar_a_voz_por_texto(message):
        return

    texto = message.content
    respuesta = await responder(texto)

    estado = cargar_estado()

    if estado["tts"]:
        archivo = generar_tts(respuesta)
        await message.channel.send(file=discord.File(archivo))
    else:
        await message.channel.send(respuesta)

    if estado["conversacion_continua"]:
        await message.channel.send("¿Quieres que siga?")

    await bot.process_commands(message)

# -----------------------------------
# INICIAR BOT
# -----------------------------------
bot.run(os.getenv("DISCORD_TOKEN"))
