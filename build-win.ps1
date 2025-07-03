# Función para verificar si un comando está disponible
function Test-CommandExists {
    param ($command)
    $oldPreference = $ErrorActionPreference
    $ErrorActionPreference = 'stop'
    try { if (Get-Command $command) { return $true } }
    catch { return $false }
    finally { $ErrorActionPreference = $oldPreference }
}

# Verificar que Python esté instalado
Write-Host "Verificando instalación de Python..." -ForegroundColor Cyan
if (-not (Test-CommandExists python)) {
    Write-Host "ERROR: Python no está instalado. Por favor, instala Python desde https://www.python.org/" -ForegroundColor Red
    Write-Host "Presiona cualquier tecla para salir..." -ForegroundColor Red
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

# Verificar y crear el entorno virtual si no existe
Write-Host "Verificando entorno virtual..." -ForegroundColor Cyan
if (-not (Test-Path -Path ".venv")) {
    Write-Host "Creando entorno virtual..." -ForegroundColor Yellow
    python -m venv .venv
    if (-not $?) {
        Write-Host "ERROR: No se pudo crear el entorno virtual." -ForegroundColor Red
        Write-Host "Presiona cualquier tecla para salir..." -ForegroundColor Red
        $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        exit 1
    }
}

# Activar el entorno virtual
Write-Host "Activando entorno virtual..." -ForegroundColor Cyan
& .\.venv\Scripts\Activate.ps1
if (-not $?) {
    Write-Host "ERROR: No se pudo activar el entorno virtual." -ForegroundColor Red
    Write-Host "Presiona cualquier tecla para salir..." -ForegroundColor Red
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

Write-Host "Compilando MoveMouse para Windows..." -ForegroundColor Green
try {
    Write-Host "Instalando dependencias..." -ForegroundColor Cyan
    pip install keyboard==0.13.5 pyinstaller==6.14.1
    
    Write-Host "Compilando aplicación..." -ForegroundColor Cyan
    pyinstaller windows.spec
    
    Write-Host "¡Compilación completada!" -ForegroundColor Green
    Write-Host "El ejecutable se encuentra en la carpeta dist/" -ForegroundColor Yellow
}
catch {
    Write-Host "Error durante la compilación: $_" -ForegroundColor Red
}
finally {
    # Desactivar el entorno virtual
    deactivate
}

Write-Host "Presiona cualquier tecla para salir..." -ForegroundColor Cyan
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") 