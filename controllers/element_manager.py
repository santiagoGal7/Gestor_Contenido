from utils import screencontroller as screen
from utils import validateData as validate

def _generar_nuevo_id(coleccion):
    """Genera un nuevo ID único para un elemento (ej: E001, E002, ...)."""
    if not coleccion:
        return "E001"
    ids_numericos = [int(item['id'][1:]) for item in coleccion if item['id'].startswith('E') and item['id'][1:].isdigit()]
    if not ids_numericos:
        return "E001"
    max_id = max(ids_numericos)
    return f"E{max_id + 1:03d}"

def anadir_elemento(coleccion):
    """Gestiona el flujo para añadir un nuevo elemento. Devuelve True si se añade, False si se cancela."""
    screen.limpiar_pantalla()
    categorias = ["Libro", "Película", "Música"]
    idx_cat = screen.crear_menu_interactivo(categorias, "Selecciona la categoría:")
    categoria = categorias[idx_cat]
    label_responsable = "Autor" if categoria == "Libro" else "Director" if categoria == "Película" else "Artista"

    while True:
        titulo = screen.obtener_input_valido("Título:", validacion=lambda t: not validate.titulo_existe(t, coleccion), msg_error="Ya existe un elemento con este título.")
        if titulo is None: break
        responsable = screen.obtener_input_valido(f"{label_responsable}:")
        if responsable is None: break
        genero = screen.obtener_input_valido("Género:")
        if genero is None: break
        valoracion_str = screen.obtener_input_valido("Valoración (1-5, opcional):", es_opcional=True, validacion=validate.es_valoracion_valida, msg_error="Debe ser un número entre 1 y 5.")
        if valoracion_str is None: break

        valoracion = int(valoracion_str) if valoracion_str else None
        nuevo_item = {"id": _generar_nuevo_id(coleccion), "categoria": categoria, "titulo": titulo, "responsable": responsable, "genero": genero, "valoracion": valoracion}
        coleccion.append(nuevo_item)
        screen.mostrar_mensaje("Elemento añadido con éxito.", "exito")
        return True

    screen.mostrar_mensaje("Operación cancelada por el usuario.", "aviso")
    return False
