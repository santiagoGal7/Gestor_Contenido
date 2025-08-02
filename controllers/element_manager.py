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
    if idx_cat == -1:
        screen.mostrar_mensaje("Operación cancelada.", "aviso")
        return False
    categoria = categorias[idx_cat]
    label_responsable = "Autor" if categoria == "Libro" else "Director" if categoria == "Película" else "Artista"
    titulo = screen.obtener_input_valido(
        "Título:",
        validacion=lambda t: not validate.titulo_existe(t, coleccion),
        msg_error="Ya existe un elemento con este título."
    )
    if titulo is None:
        screen.mostrar_mensaje("Operación cancelada.", "aviso")
        return False

    responsable = screen.obtener_input_valido(
        f"{label_responsable}:",
        validacion=validate.es_texto_sin_simbolos,
        msg_error="Entrada inválida. Solo puede contener letras y números."
    )
    if responsable is None:
        screen.mostrar_mensaje("Operación cancelada.", "aviso")
        return False

    genero = screen.obtener_input_valido(
        "Género:",
        validacion=validate.es_genero_valido,
        msg_error="Género inválido. Solo puede contener letras."
    )
    if genero is None:
        screen.mostrar_mensaje("Operación cancelada.", "aviso")
        return False

    valoracion_str = screen.obtener_input_valido(
        "Valoración (1-5, opcional):", 
        es_opcional=True, 
        validacion=validate.es_valoracion_valida, 
        msg_error="Debe ser un número entre 1 y 5."
    )
    if valoracion_str is None:
        screen.mostrar_mensaje("Operación cancelada.", "aviso")
        return False
    valoracion = int(valoracion_str) if valoracion_str else None
    nuevo_item = {
        "id": _generar_nuevo_id(coleccion), 
        "categoria": categoria, 
        "titulo": titulo, 
        "responsable": responsable, 
        "genero": genero, 
        "valoracion": valoracion
    }
    coleccion.append(nuevo_item)
    screen.mostrar_mensaje("Elemento añadido con éxito.", "exito")
    return True

def editar_elemento(coleccion):
    if not coleccion:
        screen.mostrar_mensaje("No hay elementos para editar.", "aviso")
        return False
    opciones = [f"{item.get('titulo', 'Sin Título')} ({item.get('categoria', 'N/A')})" for item in coleccion]
    opciones.append(f"{styles.COLOR_YELLOW}Cancelar Edición{styles.COLOR_RESET}") 
    idx_item = screen.main_menu_set(opciones, "Selecciona un elemento para editar:")
    if idx_item == -1 or idx_item == len(opciones) - 1:
        screen.mostrar_mensaje("Edición cancelada.", "aviso")
        return False
    item_editar = coleccion[idx_item]
    cambiox = False
    while True:
        campos_editar = {
            "Título": "titulo",
            "Responsable": "responsable",
            "Género": "genero",
            "Valoración": "valoracion"
        }
        opciones_edicion = list(campos_editar.keys())
        opciones_edicion.append(f"{styles.COLOR_GREEN}Guardar Cambios y Salir{styles.COLOR_RESET}")
        titulo_actual = item_editar.get('titulo', 'N/A')
        idx_campo = screen.main_menu_set(opciones_edicion, f"Editando: {titulo_actual}")
        if idx_campo == len(opciones_edicion) - 1:
            break 
        if idx_campo == -1:
             cambiox = False 
             break
        campo_display = opciones_edicion[idx_campo]
        campo_real = campos_editar[campo_display]
        valor_actual = item_editar.get(campo_real)
        prompt_valor_actual = f" (actual: {valor_actual if valor_actual is not None else 'N/A'})"
        prompt = f"Nuevo {campo_display}{prompt_valor_actual}:"
        nuevo_valor = None
        if campo_real == 'titulo':
            nuevo_valor = screen.obtener_input_valido(
                prompt,
                validacion=lambda t: not validate.titulo_existe(t, coleccion, item_editar['id']),
                msg_error="Ya existe otro elemento con ese título."
            )
        elif campo_real == 'responsable':
            nuevo_valor = screen.obtener_input_valido(
                prompt,
                validacion=validate.es_texto_sin_simbolos,
                msg_error="Solo puede contener letras y números."
            )
        elif campo_real == 'genero':
            nuevo_valor = screen.obtener_input_valido(
                prompt,
                validacion=validate.es_genero_valido,
                msg_error="Solo puede contener letras."
            )
        elif campo_real == 'valoracion':
            nuevo_valor_str = screen.obtener_input_valido(
                prompt, es_opcional=True,
                validacion=validate.es_valoracion_valida,
                msg_error="Debe ser un número entre 1 y 5."
            )
            if nuevo_valor_str is not None:
                nuevo_valor = int(nuevo_valor_str) if nuevo_valor_str else None
        if nuevo_valor is not None:
            item_editar[campo_real] = nuevo_valor
            cambiox = True
            screen.mostrar_mensaje(f"Campo '{campo_display}' actualizado.", "exito", con_pausa=False)
            import time
            time.sleep(1.5)
    if cambiox:
        screen.mostrar_mensaje("Cambios guardados con éxito en la sesión.", "exito")
    else:
        screen.mostrar_mensaje("No se realizó ningún cambio.", "aviso")
    return cambiox

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