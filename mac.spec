# -*- mode: python ; coding: utf-8 -*-

import os
import sys
import json

# Cargar información de versión desde el archivo JSON
with open('version.json', 'r') as f:
    version_info = json.load(f)

block_cipher = None

a = Analysis(
    ['mm_mac.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
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

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name=f'{version_info["original_filename"]}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=True,  # Habilitar emulación de argumentos para macOS
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='mm.icns',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=True,
    upx=True,
    upx_exclude=[],
    name=f'{version_info["original_filename"]}',
)

# Para crear una aplicación macOS (.app)
app = BUNDLE(
    coll,
    name=f'{version_info["product_name"]}.app',
    icon='mm.icns',
    bundle_identifier=version_info["bundle_identifier"],
    info_plist={
        'CFBundleShortVersionString': version_info["version"],
        'CFBundleVersion': version_info["version"],
        'NSHumanReadableCopyright': version_info["copyright"],
        'NSHighResolutionCapable': 'True',
        'LSBackgroundOnly': 'False',
        'LSUIElement': 'False',
    }
) 