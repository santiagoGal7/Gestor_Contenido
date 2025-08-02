import re

def titulo_existe(titulo, coleccion, id_actual=None):
    titulo_limpio = titulo.strip()
    for item in coleccion:
        if id_actual and item['id'] == id_actual:
            continue
        if item['titulo'].lower() == titulo_limpio.lower():
            return True
    return False

def es_valoracion_valida(valoracion_str):
    valoracion_limpia = valoracion_str.strip()
    if not valoracion_limpia.isdigit():
        return False
    valoracion = int(valoracion_limpia)
    return 1 <= valoracion <= 5

def es_texto_sin_simbolos(texto):
    texto_limpio = texto.strip()
    if not texto_limpio:
        return False
    return bool(re.match(r'^[a-zA-Z0-9 ]+$', texto_limpio))

def es_genero_valido(texto):
    texto_limpio = texto.strip()
    if not texto_limpio:
        return False
    # Permite espacios internos, como en "Ciencia Ficcion"
    return bool(re.match(r'^[a-zA-Z ]+$', texto_limpio))