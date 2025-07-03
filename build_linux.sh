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

# Verificar si pip está instalado
if ! check_command "pip3"; then
    echo -e "${RED}Error: pip3 no está instalado. Normalmente viene con Python3.${NC}"
    echo -e "${YELLOW}Puedes instalarlo con:${NC}"
    echo -e "  - Ubuntu/Debian: sudo apt install python3-pip"
    echo -e "  - Fedora: sudo dnf install python3-pip"
    echo -e "  - Arch Linux: sudo pacman -S python-pip${NC}"
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

echo -e "${GREEN}Compilando MoveMouse para Linux...${NC}"

# Comprobar si PyInstaller está instalado
if ! python3 -c "import PyInstaller" &> /dev/null; then
    echo -e "${YELLOW}Instalando PyInstaller...${NC}"
    pip install pyinstaller==6.14.1
fi

echo -e "${YELLOW}Instalando dependencias...${NC}"
pip install python-xlib==0.33 pynput==1.7.6 pyinstaller==6.14.1

echo -e "${YELLOW}Compilando aplicación...${NC}"
pyinstaller linux.spec

# Comprobar si UPX está instalado para mejor compresión
if ! command -v upx &> /dev/null; then
    echo -e "${YELLOW}Tip: Para una mejor compresión, considera instalar UPX:${NC}"
    echo -e "  - En Ubuntu/Debian: sudo apt-get install upx"
    echo -e "  - En Fedora: sudo dnf install upx"
    echo -e "  - En Arch Linux: sudo pacman -S upx"
fi

# Verificar si la compilación fue exitosa
if [ -f "dist/MM" ]; then
    echo -e "${GREEN}¡Compilación completada con éxito!${NC}"
    echo -e "${YELLOW}El ejecutable está disponible en: dist/MM${NC}"
    
    # Dar permisos de ejecución
    chmod +x dist/MM
    
    echo -e "${YELLOW}Para ejecutar la aplicación:${NC}"
    echo -e "./dist/MM"
else
    echo -e "${RED}Error en la compilación. Verifica los mensajes anteriores.${NC}"
fi

# Desactivar el entorno virtual
deactivate 