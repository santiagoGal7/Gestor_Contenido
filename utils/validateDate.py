def titulo_existe(titulo, coleccion, id_actual=None):

    for item in coleccion:
        if id_actual and item['id'] == id_actual:
            continue
        if item['titulo'].lower() == titulo.lower():
            return True
    return False

def es_valoracion_valida(valoracion_str):
    if not valoracion_str.isdigit():
        return False
    valoracion = int(valoracion_str)
    return 1 <= valoracion <= 5