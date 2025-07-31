from utils import screencontroller as screen

def buscar_elemento(coleccion):
    if not coleccion:
        screen.mostrar_mensaje("No hay elementos en la colección para buscar.", "aviso")
        return

    criterios = ["Por Título", "Por Responsable", "Por Género"]
    idx = screen.main_menu_set(criterios, "Selecciona un criterio de búsqueda:")
    criterio_key = criterios[idx].split(" ")[-1].lower()
    termino = screen.obtener_input_valido(f"Buscar {criterio_key.capitalize()} que contenga:")
    
    if termino is None:
        screen.mostrar_mensaje("Búsqueda cancelada.", "aviso")
        return
        
    resultados = [item for item in coleccion if termino.lower() in str(item.get(criterio_key, '')).lower()]
    screen.mostrar_tabla(resultados, f"Resultados para '{termino}'")


def ver_elementos_por_categoria(coleccion):
    if not coleccion:
        screen.mostrar_mensaje("La colección está vacía.", "aviso")
        return
        
    categorias_disponibles = sorted(list(set([item['categoria'] for item in coleccion])))
    if not categorias_disponibles:
        screen.mostrar_mensaje("No hay categorías para mostrar.", "aviso")
        return
        
    idx = screen.main_menu_set(categorias_disponibles, "Selecciona una categoría:")
    categoria_seleccionada = categorias_disponibles[idx]
    
    filtrados = [item for item in coleccion if item['categoria'] == categoria_seleccionada]
    screen.mostrar_tabla(filtrados, f"Categoría: {categoria_seleccionada}")