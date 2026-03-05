import sys
import os

def get_base_path():
    """Obtiene la ruta base para cargar recursos (desarrollo o PyInstaller)."""
    if getattr(sys, 'frozen', False):
        # Si se ejecuta como un ejecutable compilado por PyInstaller
        return sys._MEIPASS
    # Si se ejecuta como un script normal
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_resource_path(relative_path):
    """Obtiene la ruta absoluta para un recurso genérico."""
    return os.path.join(get_base_path(), relative_path)

def image_path(filename):
    """Obtiene la ruta absoluta para una imagen en 'assets/images/'."""
    return os.path.join(get_base_path(), "assets", "images", filename)

def master_image_path(filename):
    """Obtiene la ruta absoluta para una imagen en 'assets/images/png_master/'."""
    return os.path.join(get_base_path(), "assets", "images", "png_master", filename)

def locale_path(filename):
    """Obtiene la ruta absoluta para un archivo de idioma en 'assets/locales/'."""
    return os.path.join(get_base_path(), "assets", "locales", filename)
