# MoveMouse

Este proyecto consiste en una aplicación multiplataforma que mueve el cursor del mouse automáticamente en intervalos regulares. Útil para evitar que la pantalla se bloquee por inactividad o para mantener la sesión activa en aplicaciones que se desconectan por tiempo de inactividad.

## Características

- Mueve el cursor en intervalos de tiempo configurables
- Centra el cursor en la pantalla al iniciar
- Realiza pequeños movimientos aleatorios
- Funciona en Windows, macOS y Linux
- Fácil de detener con teclas específicas según la plataforma

## Archivos del proyecto

- **Multiplataforma**: `version.json` (configuración compartida para versiones)
- **Windows**: `mm_windows.py` y `windows.spec`
- **macOS**: `mm_mac.py` y `mac.spec`
- **Linux**: `mm_linux.py` y `linux.spec`

## Gestión de versiones

El proyecto utiliza un único archivo `version.json` para gestionar las versiones en todas las plataformas. Para actualizar la versión, simplemente modifica este archivo y vuelve a compilar:

```json
{
    "version": "1.0.0",
    "version_tuple": [1, 0, 0, 0],
    "file_description": "MoveMouse - Mantiene activo el cursor",
    "company_name": "acamus79",
    "product_name": "MoveMouse",
    "copyright": "© 2025. Todos los derechos reservados.",
    "original_filename": "MouseMover",
    "internal_name": "MouseMover",
    "bundle_identifier": "com.mousemover.app"
}
```

## Scripts de ejecución y compilación

Todos los scripts verifican automáticamente que Python esté instalado, crean un entorno virtual si es necesario, instalan todas las dependencias requeridas, y ejecutan o compilan el programa dentro del entorno aislado.

### Windows
- **Ejecutar**: 
  - `run_windows.bat` - Archivo batch para ejecutar
  - `Run-Windows.ps1` - Script PowerShell para ejecutar
- **Compilar**:
  - `build_windows.bat` - Archivo batch para compilar
  - `Build-Windows.ps1` - Script PowerShell para compilar

### macOS
- **Ejecutar**: `run_mac.sh` (usar `chmod +x run_mac.sh` para dar permisos)
- **Compilar**: `build_mac.sh` (usar `chmod +x build_mac.sh` para dar permisos)

### Linux
- **Ejecutar**: `run_linux.sh` (usar `chmod +x run_linux.sh` para dar permisos)
- **Compilar**: `build_linux.sh` (usar `chmod +x build_linux.sh` para dar permisos)

## Requisitos

¡No necesitas instalar nada! Los scripts de ejecución y compilación verificarán automáticamente los requisitos e instalarán las dependencias necesarias en un entorno virtual.

Si prefieres instalar manualmente las dependencias:

```bash
# Para todas las plataformas
pip install -r requirements_all.txt
```

O específicos para cada plataforma:

**Windows**:
```bash
pip install keyboard pyinstaller
```

**macOS**:
```bash
pip install pyobjc-core pyobjc-framework-Quartz pyinstaller
```

**Linux**:
```bash
pip install python-xlib pyinstaller
```

## Uso

### Ejecución del script

Simplemente ejecuta el script correspondiente a tu plataforma y se encargará de todo:

**Windows**:
```bash
# Usando batch
run_windows.bat

# Usando PowerShell
.\Run-Windows.ps1

# Directamente con Python
python mm_windows.py
```
Presiona `F12` para detener.

**macOS**:
```bash
# Usando shell script
./run_mac.sh

# Directamente con Python
python3 mm_mac.py
```
Presiona `Ctrl+C` o `Cmd+Q` para detener.

**Linux**:
```bash
# Usando shell script
./run_linux.sh

# Directamente con Python
python3 mm_linux.py
```
Presiona `Ctrl+C` para detener.

### Compilación del ejecutable

Los scripts de compilación automatizan todo el proceso, incluyendo la creación de un entorno virtual, instalación de dependencias y compilación:

**Windows**:
```bash
# Usando batch
build_windows.bat

# Usando PowerShell
.\Build-Windows.ps1

# Directamente con PyInstaller
pyinstaller windows.spec
```
El ejecutable se generará en la carpeta `dist`.

**macOS**:
```bash
# Usando shell script
./build_mac.sh

# Directamente con PyInstaller
pyinstaller mac.spec
```
El ejecutable se generará como una aplicación `.app` en la carpeta `dist`.

**Linux**:
```bash
# Usando shell script
./build_linux.sh

# Directamente con PyInstaller
pyinstaller linux.spec
```
El ejecutable se generará en la carpeta `dist`.

## Notas importantes

### Windows
- Utiliza la biblioteca `keyboard` para la detección de teclas
- Requiere que `libffi-8.dll` esté presente para funcionar correctamente
- Los scripts automatizan la creación del entorno virtual con `venv`

### macOS
- Necesitas crear un archivo de icono `.icns` si deseas un icono personalizado
- La aplicación puede requerir permisos de accesibilidad
- Para otorgar permisos: Preferencias del Sistema → Seguridad y Privacidad → Privacidad → Accesibilidad

### Linux
- Funciona con X11, puede tener problemas con Wayland
- En algunas distribuciones puede necesitar permisos adicionales
- Los scripts verifican automáticamente el tipo de sesión (X11/Wayland)

## Personalización

Para modificar el intervalo de tiempo o el rango de movimiento, edita las constantes al inicio de cada archivo:

```python
INTERVAL = 10  # Tiempo en segundos entre movimientos
RANGE_MOVEMENT = 10  # Rango máximo de movimiento en píxeles
```

## Licencia

Este proyecto está bajo la licencia MIT.

## Contribuciones

Las contribuciones son bienvenidas. Si encuentras algún problema o tienes sugerencias, por favor abre un issue o envía un pull request. 