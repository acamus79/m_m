# mm_mac.py
# Este programa mueve el cursor en macOS en intervalos de tiempo definidos
# La posición del cursor se centra en la pantalla al inicio
# El movimiento del cursor es aleatorio dentro de un rango determinado
# Se puede detener presionando F12

import time
import random
import sys
import os
import signal
import threading
from Quartz import CGDisplayBounds, CGMainDisplayID, CGPoint
from Quartz.CoreGraphics import CGEventCreateMouseEvent, CGEventPost, kCGEventMouseMoved, kCGHIDEventTap, kCGEventLeftMouseDown, kCGEventLeftMouseUp
from pynput import keyboard

# Configuración del intervalo (en segundos) y el rango de movimiento
INTERVAL = 10  # Mueve el cursor cada 10 segundos
RANGE_MOVEMENT = 10  # Movimiento máximo en píxeles

# Variable para controlar la ejecución del bucle
running = True

def handle_signal(sig, frame):
    """Manejador de señal para detener el programa con Ctrl+C"""
    global running
    running = False
    print("Programa detenido por el usuario.")
    sys.exit(0)

def get_screen_size():
    """Obtener el tamaño de la pantalla principal"""
    mainMonitor = CGDisplayBounds(CGMainDisplayID())
    return (int(mainMonitor.size.width), int(mainMonitor.size.height))

def move_mouse_to(x, y):
    """Mover el cursor a una posición específica"""
    # Crear un evento de movimiento del mouse
    event = CGEventCreateMouseEvent(
        None, kCGEventMouseMoved, CGPoint(x, y), 0)
    
    # Enviar el evento
    CGEventPost(kCGHIDEventTap, event)

def center_mouse():
    """Centrar el mouse en la pantalla"""
    width, height = get_screen_size()
    center_x = width // 2
    center_y = height // 2
    move_mouse_to(center_x, center_y)
    print(f"Ratón centrado en la posición ({center_x}, {center_y})")

def move_cursor():
    """Mover el cursor de forma aleatoria"""
    # Obtener la posición actual del cursor
    event = CGEventCreateMouseEvent(None, kCGEventMouseMoved, CGPoint(0, 0), 0)
    currentLoc = CGEventPost(kCGHIDEventTap, event)
    
    # En macOS, necesitamos una manera diferente de obtener la posición actual
    # Esta es una forma aproximada basada en la posición anterior
    # En una implementación real, se debería usar NSEvent
    
    # Obtener tamaño de pantalla para evitar mover fuera de los límites
    width, height = get_screen_size()
    
    # Generar movimiento aleatorio
    dx = random.randint(-RANGE_MOVEMENT, RANGE_MOVEMENT)
    dy = random.randint(-RANGE_MOVEMENT, RANGE_MOVEMENT)
    
    # Calcular nueva posición
    # Como no tenemos la posición exacta actual, movemos relativamente al centro
    center_x = width // 2
    center_y = height // 2
    
    new_x = min(max(center_x + dx, 0), width)
    new_y = min(max(center_y + dy, 0), height)
    
    # Mover el cursor a la nueva posición
    move_mouse_to(new_x, new_y)

def stop_program():
    global running
    running = False
    print("Programa detenido por pulsación de F12.")

def on_key_press(key):
    if key == keyboard.Key.f12:
        stop_program()
        return False  # Detener la escucha

def keyboard_listener():
    with keyboard.Listener(on_press=on_key_press) as listener:
        listener.join()

def main():
    # Configurar manejo de señal para Ctrl+C
    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)
    
    # Iniciar thread para escuchar la tecla F12
    listener_thread = threading.Thread(target=keyboard_listener)
    listener_thread.daemon = True
    listener_thread.start()
    
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
        sys.exit(1)

if __name__ == "__main__":
    main() 