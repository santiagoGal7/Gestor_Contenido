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