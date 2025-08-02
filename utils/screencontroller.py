import os
import sys
from utils import styles

try:
    import msvcrt
    def _getch():
        key = msvcrt.getch()
        if key in (b'\x00', b'\xe0'):
            char = msvcrt.getch()
            if char == b'H': return "UP"
            if char == b'P': return "DOWN"
        elif key == b'\r': return "ENTER"
        elif key == b'\x1b': return "ESC"
        return None
except ImportError:
    import tty, termios
    def _getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
            if ch == '\x1b':
                ch += sys.stdin.read(2)
                if ch == '\x1b[A': return "UP"
                if ch == '\x1b[B': return "DOWN"
                return "ESC"
            elif ch in ('\r', '\n'): return "ENTER"
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return None

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def pausar_pantalla(mensaje="Presiona Enter para continuar..."):
    print(f"\n{styles.COLOR_YELLOW}{mensaje}{styles.COLOR_RESET}")
    input()

def main_menu_set(opciones, titulo):
    seleccion_actual = 0
    while True:
        limpiar_pantalla()
        print(f"{styles.COLOR_BOLD}{styles.COLOR_BLUE}{titulo}{styles.COLOR_RESET}\n")
        for i, opcion in enumerate(opciones):
            if i == seleccion_actual:
                print(f" {styles.COLOR_GREEN}▶ {opcion}{styles.COLOR_RESET}")
            else:
                print(f"   {opcion}")
        print(f"\n{styles.COLOR_MAGENTA}{styles.COLOR_BOLD}(Usa las flechas ▲/▼ y Enter para seleccionar){styles.COLOR_RESET}")

        tecla = None
        while tecla not in ["UP", "DOWN", "ENTER", "ESC"]:
            tecla = _getch()

        if tecla == "UP":
            seleccion_actual = (seleccion_actual - 1 + len(opciones)) % len(opciones)
        elif tecla == "DOWN":
            seleccion_actual = (seleccion_actual + 1) % len(opciones)
        elif tecla == "ENTER":
            limpiar_pantalla()
            return seleccion_actual
        elif tecla == "ESC":
            return -1

def obtener_input_valido(prompt, es_opcional=False, validacion=None, msg_error="Entrada inválida."):

    MOVE_UP = '\033[F'
    CLEAR_LINE = '\033[K'
    
    print(f"\n{styles.COLOR_YELLOW}(Escribe !cancelar para anular la operación){styles.COLOR_RESET}")

    while True:
        print(f"{styles.COLOR_CYAN}{prompt}{styles.COLOR_RESET}", end=" ")
        entrada = input()

        if entrada == '!cancelar':
            print(f"{MOVE_UP}{CLEAR_LINE}" * 2, end='')
            return None

        entrada_limpia = entrada.strip()

        if not entrada_limpia and not es_opcional:
            error_a_mostrar = "Este campo no puede estar vacío."
        elif es_opcional and not entrada_limpia:
            print(f"{MOVE_UP}{CLEAR_LINE}" * 2, end='')
            return ""
        elif validacion and not validacion(entrada_limpia):
            error_a_mostrar = f"Error: {msg_error}"
        else:
            print(f"{MOVE_UP}{CLEAR_LINE}" * 2, end='')
            print(f"{styles.COLOR_CYAN}{prompt}{styles.COLOR_RESET} {styles.COLOR_GREEN}{entrada_limpia}{styles.COLOR_RESET}")
            return entrada_limpia

        print(f"{MOVE_UP}{CLEAR_LINE}", end='')
        print(f"{styles.COLOR_CYAN}{prompt}{styles.COLOR_RED} {error_a_mostrar}{styles.COLOR_RESET}")
        input(f"{styles.COLOR_YELLOW}Presiona ENTER para volver a intentarlo...{styles.COLOR_RESET}")
        
        print(f"{MOVE_UP}{CLEAR_LINE}" * 2, end='')

def mostrar_mensaje(mensaje, tipo="info", con_pausa=True):
    color_map = {
        "exito": styles.COLOR_GREEN, "aviso": styles.COLOR_YELLOW,
        "error": styles.COLOR_RED, "info": styles.COLOR_BLUE
    }
    print(f"\n{color_map.get(tipo, styles.COLOR_BLUE)}{styles.COLOR_BOLD}{mensaje}{styles.COLOR_RESET}")
    if con_pausa:
        pausar_pantalla()

def mostrar_tabla(coleccion, titulo):
    limpiar_pantalla()
    if not coleccion:
        mostrar_mensaje(f"No hay elementos para mostrar en esta vista.", "aviso")
        return

    print(f"{styles.COLOR_BOLD}{styles.COLOR_BLUE}{titulo}{styles.COLOR_RESET}\n")
    cabeceras = ["ID", "Categoría", "Título", "Responsable", "Género", "Valoración"]

    print(f"{styles.COLOR_GREEN}{cabeceras[0]:<5} {cabeceras[1]:<10} {cabeceras[2]:<30} {cabeceras[3]:<25} {cabeceras[4]:<20} {cabeceras[5]:<10}{styles.COLOR_RESET}")
    print("-" * 105)

    for item in coleccion:
        valoracion = item.get('valoracion') or 'N/A'
        print(
            f"{item.get('id', 'N/A'):<5} "
            f"{item.get('categoria', 'N/A'):<10} "
            f"{item.get('titulo', 'N/A'):<30.30} "
            f"{item.get('responsable', 'N/A'):<25.25} "
            f"{item.get('genero', 'N/A'):<20.20} "
            f"{str(valoracion):<10}"
        )
    pausar_pantalla()