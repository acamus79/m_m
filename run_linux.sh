#!/bin/bash

# Colores para la salida
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Función para verificar comandos
check_command() {
    if ! command -v "$1" &> /dev/null; then
        echo -e "${RED}Error: $1 no está instalado.${NC}"
        return 1
    fi
    return 0
}

echo -e "${CYAN}Verificando instalación de Python...${NC}"
if ! check_command "python3"; then
    echo -e "${RED}Error: Python3 no está instalado. Por favor, instala Python3.${NC}"
    echo -e "${YELLOW}En la mayoría de las distribuciones Linux puedes instalarlo con:${NC}"
    echo -e "  - Ubuntu/Debian: sudo apt install python3 python3-pip python3-venv"
    echo -e "  - Fedora: sudo dnf install python3 python3-pip"
    echo -e "  - Arch Linux: sudo pacman -S python python-pip${NC}"
    exit 1
fi

# Verificar y crear el entorno virtual si no existe
echo -e "${CYAN}Verificando entorno virtual...${NC}"
if [ ! -d ".venv" ]; then
    echo -e "${YELLOW}Creando entorno virtual...${NC}"
    python3 -m venv .venv
    if [ $? -ne 0 ]; then
        echo -e "${RED}Error: No se pudo crear el entorno virtual.${NC}"
        echo -e "${YELLOW}¿Está instalado el módulo venv? Instálalo con:${NC}"
        echo -e "  - Ubuntu/Debian: sudo apt install python3-venv"
        echo -e "  - Fedora: sudo dnf install python3-virtualenv"
        echo -e "  - Arch Linux: python-virtualenv ya está incluido con python${NC}"
        exit 1
    fi
fi

# Activar el entorno virtual
echo -e "${CYAN}Activando entorno virtual...${NC}"
source .venv/bin/activate
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: No se pudo activar el entorno virtual.${NC}"
    exit 1
fi

# Instalar dependencias
echo -e "${CYAN}Instalando dependencias...${NC}"
pip install python-xlib==0.33 pynput==1.7.6

echo -e "${GREEN}Iniciando MoveMouse para Linux...${NC}"
echo -e "${YELLOW}Presiona F12 para detener la aplicación.${NC}"

# Comprobar si estamos en Wayland o X11
session_type=$(echo $XDG_SESSION_TYPE)
if [ "$session_type" == "wayland" ]; then
    echo -e "${YELLOW}ADVERTENCIA: Estás usando Wayland. Esta aplicación está diseñada para X11 y puede no funcionar correctamente.${NC}"
    echo -e "${YELLOW}Para obtener mejores resultados, considera cambiar a una sesión X11.${NC}"
    read -p "¿Deseas continuar de todas formas? (s/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Ss]$ ]]; then
        echo -e "${RED}Operación cancelada.${NC}"
        deactivate
        exit 1
    fi
fi

# Dar permiso de ejecución al script si no lo tiene
if [ ! -x "mm_linux.py" ]; then
    chmod +x mm_linux.py
fi

# Ejecutar el script
python3 mm_linux.py

# Desactivar el entorno virtual al finalizar
deactivate

echo -e "${GREEN}Programa terminado.${NC}" 