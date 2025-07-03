@echo off
echo Verificando instalacion de Python...

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python no esta instalado. Por favor, instala Python desde https://www.python.org/
    pause
    exit /b 1
)

echo Verificando entorno virtual...
if not exist ".venv" (
    echo Creando entorno virtual...
    python -m venv .venv
)

echo Activando entorno virtual...
call .venv\Scripts\activate.bat

echo Instalando dependencias...
pip install keyboard==0.13.5 pyinstaller==6.14.1

echo Compilando MoveMouse para Windows...
pyinstaller windows.spec

echo Compilacion completada. El ejecutable se encuentra en la carpeta dist/
call .venv\Scripts\deactivate.bat
pause 