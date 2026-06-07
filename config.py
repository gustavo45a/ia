def elegir_modelo(texto: str) -> str:
    texto_l = texto.lower()

    if len(texto) < 80:
        return "fast"

    palabras_pro = ["analiza", "explica", "detallado", "profundo", "razona", "describe", "plan", "ensayo"]
    if any(p in texto_l for p in palabras_pro):
        return "pro"

    return "fast"
