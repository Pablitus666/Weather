import os
import sys

def get_resource_path(relative_path):
    """Obtiene la ruta absoluta para recursos, compatible con PyInstaller."""
    try:
        # PyInstaller crea una carpeta temporal y guarda la ruta en _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
