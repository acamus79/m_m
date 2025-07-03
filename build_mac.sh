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

# Verificar si pip está instalado
if ! check_command "pip3"; then
    echo -e "${RED}Error: pip3 no está instalado. Normalmente viene con Python3.${NC}"
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

echo -e "${GREEN}Compilando MoveMouse para macOS...${NC}"

# Comprobar si PyInstaller está instalado
if ! python3 -c "import PyInstaller" &> /dev/null; then
    echo -e "${YELLOW}Instalando PyInstaller...${NC}"
    pip install pyinstaller==6.14.1
fi

echo -e "${YELLOW}Instalando dependencias...${NC}"
pip install pyobjc-core==10.1 pyobjc-framework-Quartz==10.1 pynput==1.7.6 pyinstaller==6.14.1

echo -e "${YELLOW}Compilando aplicación...${NC}"
pyinstaller mac.spec

# Verificar si la compilación fue exitosa
if [ -d "dist/MouseMover.app" ]; then
    echo -e "${GREEN}¡Compilación completada con éxito!${NC}"
    echo -e "${YELLOW}La aplicación está disponible en: dist/MouseMover.app${NC}"
    
    # Opcional: hacer la aplicación ejecutable
    chmod +x dist/MouseMover.app/Contents/MacOS/MM
    
    echo -e "${YELLOW}Tip: Para ejecutar la aplicación, puedes hacer doble clic en ella o ejecutar:${NC}"
    echo -e "open dist/MouseMover.app"
else
    echo -e "${RED}Error en la compilación. Verifica los mensajes anteriores.${NC}"
fi

# Desactivar el entorno virtual al finalizar
deactivate 