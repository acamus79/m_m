# mm_windows.py
# Este programa mueve el cursor en Windows en intervalos de tiempo definidos
# La posición del cursor se centra en la pantalla al inicio
# El movimiento del cursor es aleatorio dentro de un rango determinado
# Se puede detener presionando la tecla F12

import time
import random
import keyboard
import ctypes
from ctypes import wintypes

# Configuración del intervalo (en segundos) y el rango de movimiento
INTERVAL = 10  # Mueve el cursor cada 10 segundos
RANGE_MOVEMENT = 10  # Movimiento máximo en píxeles

# Variable para controlar la ejecución del bucle
running = True

# Función para centrar el ratón en la pantalla
def center_mouse():
    # Obtener dimensiones de la pantalla
    user32 = ctypes.windll.user32
    screen_width = user32.GetSystemMetrics(0)  # SM_CXSCREEN
    screen_height = user32.GetSystemMetrics(1)  # SM_CYSCREEN
    
    # Calcular el centro
    center_x = screen_width // 2
    center_y = screen_height // 2
    
    # Mover el cursor al centro
    user32.SetCursorPos(center_x, center_y)
    print(f"Ratón centrado en la posición ({center_x}, {center_y})")

# Definir estructuras y funciones de Windows API
def move_cursor():
    # Obtener la posición actual del cursor
    cursor_pos = wintypes.POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(cursor_pos))
    
    # Generar movimiento aleatorio
    dx = random.randint(-RANGE_MOVEMENT, RANGE_MOVEMENT)
    dy = random.randint(-RANGE_MOVEMENT, RANGE_MOVEMENT)
    
    # Mover el cursor a la nueva posición
    ctypes.windll.user32.SetCursorPos(cursor_pos.x + dx, cursor_pos.y + dy)

# Función que se ejecuta cuando se presiona F12
def stop_program():
    global running
    running = False
    print("Programa detenido por pulsación de F12.")

def main():
    # Registramos la tecla F12 para detener el programa
    keyboard.add_hotkey('f12', stop_program)

    try:
        print("Programa iniciado. Presiona F12 para detener.")
        
        # Centramos el ratón al inicio
        center_mouse()
        
        while running:
            # Mover el cursor
            move_cursor()
            
            # Espera antes de repetir
            time.sleep(INTERVAL)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Limpiamos los hotkeys al salir
        keyboard.unhook_all()

if __name__ == "__main__":
    main() 