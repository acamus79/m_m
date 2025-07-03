# -*- mode: python ; coding: utf-8 -*-

import os
import sys
import json

# Cargar información de versión desde el archivo JSON
with open('version.json', 'r') as f:
    version_info = json.load(f)

# Crear archivo de versión temporal para Windows
version_file = 'win_version.txt'
with open(version_file, 'w') as f:
    f.write(f'''# UTF-8
#
# For more details about fixed file info 'ffi' see:
# http://msdn.microsoft.com/en-us/library/ms646997.aspx
VSVersionInfo(
  ffi=FixedFileInfo(
    # filevers y prodvers deben ser tuplas de 4 elementos (1, 2, 3, 4)
    filevers={tuple(version_info["version_tuple"])},
    prodvers={tuple(version_info["version_tuple"])},
    # Bit mask que contiene banderas para el archivo
    mask=0x3f,
    # Banderas para el archivo
    flags=0x0,
    # Tipo de SO para el que fue diseñado
    OS=0x40004,
    # Tipo general del archivo
    fileType=0x1,
    # Función del archivo
    subtype=0x0,
    # Fecha de creación
    date=(0, 0)
    ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'{version_info["company_name"]}'),
        StringStruct(u'FileDescription', u'{version_info["file_description"]}'),
        StringStruct(u'FileVersion', u'{version_info["version"]}'),
        StringStruct(u'InternalName', u'{version_info["internal_name"]}'),
        StringStruct(u'LegalCopyright', u'{version_info["copyright"]}'),
        StringStruct(u'OriginalFilename', u'{version_info["original_filename"]}.exe'),
        StringStruct(u'ProductName', u'{version_info["product_name"]}'),
        StringStruct(u'ProductVersion', u'{version_info["version"]}')
        ])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [0x0409, 1200])])
  ]
)''')

block_cipher = None

# Obtener la ruta al DLL de Python para incluirla explícitamente
python_dll = os.path.join(os.path.dirname(sys.executable), 'python312.dll')

a = Analysis(
    ['mm_windows.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['ctypes', 'ctypes.wintypes', '_ctypes'],  # Incluir explícitamente ctypes
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['pyautogui', 'PIL', 'cv2', 'numpy', 'pandas', 'matplotlib', 'PyQt5', 'tkinter'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Agregar los DLLs necesarios para ctypes
a.binaries += [('libffi-8.dll', os.path.join(os.path.dirname(sys.executable), 'libffi-8.dll'), 'BINARY')]
a.binaries += [('python312.dll', python_dll, 'BINARY')]

# Eliminar binarios innecesarios pero conservando los esenciales
binaries_to_exclude = [
    'libopenblas', 'mkl', 'libiomp', 'libtiff', 
    'libjpeg', 'libpng', 'zlib', 'sqlite3', 'tcl', 'tk'
]

def exclude_binaries(binaries):
    result = []
    for b in binaries:
        # No excluir libffi ni archivos relacionados con ctypes
        if not any(x in b[0].lower() for x in binaries_to_exclude) or 'libffi' in b[0].lower() or '_ctypes' in b[0].lower():
            result.append(b)
    return result

a.binaries = exclude_binaries(a.binaries)

# Eliminar archivos innecesarios
a.datas = [d for d in a.datas if not any(x in d[0].lower() for x in ['README', 'LICENSE', '.pyc', '.pyo'])]

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
    strip=False,  # Cambiado a False porque strip no está disponible en Windows
    upx=True,    # Usar UPX para comprimir aún más
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version=version_file,
    icon='mm.ico',
)

# Limpieza del archivo de versión temporal
import atexit
def cleanup_version_file():
    if os.path.exists(version_file):
        try:
            os.remove(version_file)
        except:
            pass
atexit.register(cleanup_version_file) 