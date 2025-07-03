# -*- mode: python ; coding: utf-8 -*-

import os
import sys
import json

# Cargar información de versión desde el archivo JSON
with open('version.json', 'r') as f:
    version_info = json.load(f)

block_cipher = None

a = Analysis(
    ['mm_linux.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['Xlib', 'Xlib.display', 'Xlib.X', 'Xlib.ext.xtest'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['pyautogui', 'PIL', 'cv2', 'numpy', 'pandas', 'matplotlib', 'PyQt5', 'tkinter'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Eliminar binarios innecesarios
binaries_to_exclude = [
    'libopenblas', 'mkl', 'libiomp', 'libtiff', 
    'libjpeg', 'libpng', 'zlib', 'sqlite3', 'tcl', 'tk'
]

def exclude_binaries(binaries):
    result = []
    for b in binaries:
        if not any(x in b[0].lower() for x in binaries_to_exclude):
            result.append(b)
    return result

a.binaries = exclude_binaries(a.binaries)

# Eliminar archivos innecesarios
a.datas = [d for d in a.datas if not any(x in d[0].lower() for x in ['README', 'LICENSE', '.pyc', '.pyo'])]

# Agregar archivo version.json como recurso
a.datas += [('version.json', 'version.json', 'DATA')]

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name=f'{version_info["original_filename"]}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,  # Linux soporta strip
    upx=True,    # Usar UPX para comprimir aún más
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='mm.png',
) 