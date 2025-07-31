import sys
import os

MainDir = os.path.dirname(os.path.abspath(__file__))
project_ruta = os.path.dirname(MainDir)
if project_ruta not in sys.path:
    sys.path.append(project_ruta)

from utils.screencontroller import menu_bymy, clean_screen, pause_screen
from utils import styles
import controllers.gestor as gestor

def main_menu():
    gestor.loading_collection()
    
    while True:
        main_tittle = "Administrador de Colección Personal"
        main_options = [
            "1. Añadir un Nuevo Elemento",
            "2. Ver Todos los Elementos",
            "3. Buscar un Elemento",
            "4. Editar un Elemento",
            "5. Eliminar un Elemento",
            "6. Ver Elementos por Categoría",
            "7. Guardar y Cargar Colección",
            "8. Salir"
        ]
        
        if gestor.unsaved_changes:
            main_options[6] += f" {styles.NEON_YELLOW}[Cambios sin guardar] {styles.RESET}"

        selection = menu_bymy(main_tittle, main_options)

        if selection == 1: gestor.show_element_table(gestor.elementos_en_memoria, "Colección Completa")
        elif selection == 2: gestor.search_element()
        elif selection == 3: gestor.edit_element()
        elif selection == 4: gestor.delete_element()
        elif selection == 5: gestor.see_elements_category()
        elif selection == 6: gestor.manage_saving_loading()
        elif selection == -1 or selection == 7: 
            if gestor.unsaved_changes:
                exit_tittle = "¿Seguro que quieres salir? Tienes cambios sin guardar."
                exit_options = ["Sí, salir sin guardar", "No, volver al programa"]
                confirmation = menu_bymy(exit_tittle, exit_options)
                if confirmation == 1: 
                    continue
            
            clean_screen()
            print(f"\n{styles.NEON_RED}{styles.BOLD}¡Hasta luego!{styles.RESET}")
            break

if __name__ == "__main__":
    main_menu()