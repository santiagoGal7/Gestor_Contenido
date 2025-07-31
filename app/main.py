import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from controllers import (
    anadir_elemento, buscar_elemento
)
from utils import screencontroller as screen
from utils import corefiles
from utils import styles

def main():
    coleccion = corefiles.leer_coleccion()
    cambios_sin_guardar = False

    opciones_menu = [
        "Añadir Nuevo Elemento",
        "Ver Todos los Elementos",
        "Buscar Elemento",
        "Editar Elemento",
        "Eliminar Elemento",
        "Ver por Categoría",
        "Guardar Cambios",
        "Salir"
    ]

    while True:
        titulo = f"{styles.COLOR_BOLD}Gestor de Contenido Personal{styles.COLOR_RESET}"
        if cambios_sin_guardar:
            titulo += f" {styles.COLOR_YELLOW}[*]{styles.COLOR_RESET}"

        seleccion = screen.crear_menu_interactivo(opciones_menu, titulo)

        if seleccion == 0:
            if anadir_elemento(coleccion):
                cambios_sin_guardar = True
        elif seleccion == 1:
            screen.mostrar_tabla(coleccion, "Colección Completa")
        elif seleccion == 2:
            buscar_elemento(coleccion)
        elif seleccion == 6:
            if cambios_sin_guardar:
                if corefiles.escribir_coleccion(coleccion):
                    screen.mostrar_mensaje("Colección guardada con éxito.", "exito")
                    cambios_sin_guardar = False
                else:
                    screen.mostrar_mensaje("Error al guardar la colección. Comprueba los permisos.", "error")
            else:
                screen.mostrar_mensaje("No hay cambios pendientes para guardar.", "aviso")

        elif seleccion == 7:
            if cambios_sin_guardar:
                opciones_salida = ["Guardar y Salir", "Salir sin Guardar", "Cancelar"]
                idx_salida = screen.crear_menu_interactivo(opciones_salida, "Hay cambios sin guardar. ¿Qué deseas hacer?")
                if idx_salida == 0:
                    corefiles.escribir_coleccion(coleccion)
                    break
                elif idx_salida == 1:
                    break
            else:
                break
    
    screen.limpiar_pantalla()
    print(f"\n{styles.COLOR_BOLD}{styles.COLOR_CYAN}¡Gracias por usar el Gestor de Contenido! ¡Hasta pronto!{styles.COLOR_RESET}\n")

if __name__ == '__main__':
    main()