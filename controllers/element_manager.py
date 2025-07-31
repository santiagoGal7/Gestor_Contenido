from utils import screencontroller as screen
from utils import validateData as validate
from utils import styles

def _generar_nuevo_id(coleccion):
    if not coleccion:
        return "E001"
    ids_numericos = [int(item['id'][1:]) for item in coleccion if item['id'].startswith('E') and item['id'][1:].isdigit()]
    if not ids_numericos:
        return "E001"
    max_id = max(ids_numericos)
    return f"E{max_id + 1:03d}"

def anadir_elemento(coleccion):
    screen.limpiar_pantalla()
    categorias = ["Libro", "Película", "Música"]
    idx_cat = screen.main_menu_set(categorias, "Selecciona la categoría:")
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

    screen.mostrar_mensaje("Operación cancelada.", "aviso")
    return False

def editar_elemento(coleccion):
    if not coleccion:
        screen.mostrar_mensaje("No hay elementos para editar.", "aviso")
        return False

    opciones = [f"{item['titulo']} ({item['categoria']})" for item in coleccion]
    idx = screen.main_menu_set(opciones, "Selecciona un elemento para editar:")
    item_a_editar = coleccion[idx]
    se_hizo_un_cambio = False

    while True:
        campos = ["Título", "Responsable", "Género", "Valoración", "[ TERMINAR EDICIÓN ]"]
        idx_campo = screen.main_menu_set(campos, f"Editando: {item_a_editar['titulo']}")
        if idx_campo == 4: break
        campo_a_editar = campos[idx_campo].lower()
        valor_actual = item_a_editar.get(campo_a_editar, "N/A")
        prompt = f"Nuevo {campos[idx_campo]} (actual: {valor_actual}):"
        
        if campo_a_editar == 'título':
            nuevo_valor = screen.obtener_input_valido(prompt, validacion=lambda t: not validate.titulo_existe(t, coleccion, item_a_editar['id']), msg_error="Ya existe otro elemento con ese título.")
        elif campo_a_editar == 'valoración':
            nuevo_valor_str = screen.obtener_input_valido(prompt, es_opcional=True, validacion=validate.es_valoracion_valida, msg_error="Debe ser un número entre 1 y 5.")
            if nuevo_valor_str is None: continue
            nuevo_valor = int(nuevo_valor_str) if nuevo_valor_str else None
        else:
            nuevo_valor = screen.obtener_input_valido(prompt)

        if nuevo_valor is None:
            screen.mostrar_mensaje(f"Edición de '{campos[idx_campo]}' cancelada.", "aviso")
            continue
        item_a_editar[campo_a_editar] = nuevo_valor
        se_hizo_un_cambio = True
        screen.mostrar_mensaje(f"Campo '{campos[idx_campo]}' actualizado.", "exito")

    if not se_hizo_un_cambio:
        screen.mostrar_mensaje("No se realizó ningún cambio.", "aviso")
    return se_hizo_un_cambio

def eliminar_elemento(coleccion):
    if not coleccion:
        screen.mostrar_mensaje("No hay elementos para eliminar.", "aviso")
        return False
    
    opciones = [f"{item['titulo']} ({item['categoria']})" for item in coleccion]
    idx = screen.main_menu_set(opciones, "Selecciona un elemento para ELIMINAR:")
    item_a_eliminar = coleccion[idx]
    confirmacion = [f"{styles.COLOR_BOLD}¡No!{styles.COLOR_RESET} Cancelar.", f"{styles.COLOR_BOLD}Sí{styles.COLOR_RESET}, eliminar este elemento"]
    idx_conf = screen.main_menu_set(confirmacion, f"¿Estás SEGURO de eliminar '{item_a_eliminar['titulo']}' de forma permanente?")
    
    if idx_conf == 1:
        coleccion.pop(idx)
        screen.mostrar_mensaje("Elemento eliminado correctamente.", "exito")
        return True
    else:
        screen.mostrar_mensaje("Eliminación cancelada.", "aviso")
        return False