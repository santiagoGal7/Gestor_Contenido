from utils import screencontroller as screen

def buscar_elemento(coleccion):
    """Flujo para buscar elementos por un criterio y término."""
    if not coleccion:
        screen.mostrar_mensaje("No hay elementos en la colección para buscar.", "aviso")
        return

    criterios = ["Por Título", "Por Responsable", "Por Género"]
    idx = screen.crear_menu_interactivo(criterios, "Selecciona un criterio de búsqueda:")
    criterio_key = criterios[idx].split(" ")[-1].lower()
    termino = screen.obtener_input_valido(f"Buscar {criterio_key.capitalize()} que contenga:")
    
    if termino is None:
        screen.mostrar_mensaje("Búsqueda cancelada.", "aviso")
        return
        
    resultados = [item for item in coleccion if termino.lower() in str(item.get(criterio_key, '')).lower()]
    screen.mostrar_tabla(resultados, f"Resultados para '{termino}'")

