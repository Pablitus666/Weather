# -*- mode: python ; coding: utf-8 -*-

"""
WeatherReport - OneFile Portable Build
Genera un único .exe 100% embebido con todos los recursos incluidos.
Optimizado para distribución profesional.
"""

from pathlib import Path

block_cipher = None

# =========================
# ANALYSIS
# =========================

a = Analysis(
    ['run.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('assets', 'assets'),
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

# =========================
# PYZ (Python Archive)
# =========================

pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher
)

# =========================
# ONE FILE EXECUTABLE
# =========================

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='WeatherReport',
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
    # RUTA DIRECTA AL ICONO OPTIMIZADO
    icon='assets\\images\\icon.ico',
)
