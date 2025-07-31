import os
import sys
from utils import styles

try:
    import msvcrt
except ImportError:
    import tty, termios
    
def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def pausar_pantalla(mensaje="Presiona Enter para continuar..."):
    print(f"\n{styles.COLOR_YELLOW}{mensaje}{styles.COLOR_RESET}")
    input()


def _getch_windows():
    key = msvcrt.getch()
    if key in (b'\x00', b'\xe0'):
        key = msvcrt.getch()
        if key == b'H': return "UP"
        if key == b'P': return "DOWN"
    elif key == b'\r': return "ENTER"
    return None

def _getch_unix():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        key = sys.stdin.read(3)
        if key == '\x1b[A': return "UP"
        if key == '\x1b[B': return "DOWN"
        if key.startswith('\r') or key.startswith('\n'): return "ENTER"
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return None

getch = _getch_windows if os.name == 'nt' else _getch_unix

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
        
        tecla = getch()
        if tecla == "UP":
            seleccion_actual = (seleccion_actual - 1 + len(opciones)) % len(opciones)
        elif tecla == "DOWN":
            seleccion_actual = (seleccion_actual + 1) % len(opciones)
        elif tecla == "ENTER":
            limpiar_pantalla()
            return seleccion_actual


def obtener_input_valido(prompt, es_opcional=False, validacion=None, msg_error="Entrada inválida."):

    print(f"\n{styles.COLOR_YELLOW}(Escribe !cancelar para anular la operación){styles.COLOR_RESET}")
    while True:
        print(f"{styles.COLOR_CYAN}{prompt}{styles.COLOR_RESET}", end=" ")
        entrada = input().strip()

        if entrada == '!cancelar':
            return None

        if not entrada and not es_opcional:
            mostrar_mensaje("Error: Este campo no puede estar vacío.", "error", con_pausa=False)
            continue
        if es_opcional and not entrada:
            return ""
        if validacion and not validacion(entrada):
            mostrar_mensaje(f"Error: {msg_error}", "error", con_pausa=False)
            continue
        return entrada

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
            f"{item['id']:<5} "
            f"{item['categoria']:<10} "
            f"{item['titulo']:<30.30} "
            f"{item['responsable']:<25.25} "
            f"{item['genero']:<20.20} "
            f"{str(valoracion):<10}"
        )
    pausar_pantalla()