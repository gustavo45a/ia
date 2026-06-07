import json

def cargar_estado():
    with open("estado.json", "r", encoding="utf-8") as f:
        return json.load(f)

def guardar_estado(estado):
    with open("estado.json", "w", encoding="utf-8") as f:
        json.dump(estado, f, indent=4)

def actualizar_emocion(texto):
    estado = cargar_estado()
    t = texto.lower()

    if "te odio" in t or "cállate" in t:
        estado["emocion"] = "enojado"
    elif "triste" in t or "solo" in t:
        estado["emocion"] = "triste"
    elif "analiza" in t or "explica" in t:
        estado["emocion"] = "serio"
    else:
        estado["emocion"] = "feliz"

    guardar_estado(estado)
    return estado["emocion"]

def actualizar_tts(texto):
    estado = cargar_estado()
    if any(p in texto.lower() for p in ["di", "habla", "voz", "tts"]):
        estado["tts"] = True
    guardar_estado(estado)
    return estado["tts"]

def actualizar_conversacion(texto):
    estado = cargar_estado()
    if texto.endswith("?") or "sigue" in texto.lower():
        estado["conversacion_continua"] = True
    guardar_estado(estado)
    return estado["conversacion_continua"]
