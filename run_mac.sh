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
    echo -e "${YELLOW}En macOS puedes instalarlo con:${NC}"
    echo -e "  - Homebrew: brew install python"
    echo -e "  - Desde python.org: https://www.python.org/downloads/macos/${NC}"
    exit 1
fi

# Verificar y crear el entorno virtual si no existe
echo -e "${CYAN}Verificando entorno virtual...${NC}"
if [ ! -d ".venv" ]; then
    echo -e "${YELLOW}Creando entorno virtual...${NC}"
    python3 -m venv .venv
    if [ $? -ne 0 ]; then
        echo -e "${RED}Error: No se pudo crear el entorno virtual.${NC}"
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
pip install pyobjc-core==10.1 pyobjc-framework-Quartz==10.1 pynput==1.7.6

echo -e "${GREEN}Iniciando MoveMouse para macOS...${NC}"
echo -e "${YELLOW}Presiona F12 para detener la aplicación.${NC}"

# Ejecutar el script
python3 mm_mac.py

# Desactivar el entorno virtual al finalizar
deactivate

echo -e "${GREEN}Programa terminado.${NC}" 