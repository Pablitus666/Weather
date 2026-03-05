# -*- mode: python ; coding: utf-8 -*-

import os
from pathlib import Path

"""
Weather - Build Profesional Optimizado
Genera un único .exe llamado 'Weather.exe' con icono embebido de alta resolución.
"""

# Obtenemos la ruta absoluta del proyecto para evitar fallos de rutas relativas en el icono
project_root = os.path.abspath(os.getcwd())
icon_path = os.path.join(project_root, 'assets', 'images', 'icon.ico')

block_cipher = None

a = Analysis(
    ['run.py'],
    pathex=[project_root],
    binaries=[],
    datas=[
        ('assets', 'assets'),
        ('assets/images/icon.ico', 'assets/images'),
        ('assets/images/loguito.ico', 'assets/images'),
    ],
    hiddenimports=[
        'PIL._tkinter_finder',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher
)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Weather',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # RUTA ABSOLUTA FORZADA PARA EL ICONO DEL EXPLORADOR
    icon=icon_path,
)
