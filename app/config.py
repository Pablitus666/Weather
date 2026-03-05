import os
import sys
import base64
from pathlib import Path
from dotenv import load_dotenv

"""
Fase 1, 3 y 4: Arquitectura de Portabilidad y Ofuscación.
Implementa detección de ruta real de PyInstaller y protección de API Key.
"""

# Fase 3 y 4: Ofuscación y Fragmentación de la API Key
# Evita que herramientas simples de 'strings' extraigan la clave fácilmente.
_K1 = "NmQxNmQyNGFi"
_K2 = "YWViYWVlOTU1"
_K3 = "N2ZmNmQyZDM3"
_K4 = "ZTkwM2I="

def _get_obfuscated_key():
    try:
        encoded = _K1 + _K2 + _K3 + _K4
        return base64.b64decode(encoded).decode()
    except Exception:
        return ""

def get_base_path():
    """
    Detecta la carpeta real del ejecutable o del script.
    Compatible con PyInstaller y ejecución normal.
    """
    if getattr(sys, "frozen", False):
        # Directorio donde reside el .exe
        return Path(sys.executable).parent
    # Directorio raíz del proyecto en desarrollo
    return Path(__file__).resolve().parent.parent

def load_api_config():
    """
    Sistema de carga jerárquica de API Key:
    1. Variable de entorno del sistema (OPENWEATHER_API_KEY)
    2. Archivo .env local (junto al ejecutable)
    3. Fallback embebido ofuscado
    """
    # 1. Prioridad: Entorno del sistema
    key = os.getenv("OPENWEATHER_API_KEY")
    if key:
        return key

    # 2. Prioridad: Archivo .env externo (Portabilidad)
    base = get_base_path()
    env_file = base / ".env"
    if env_file.exists():
        load_dotenv(env_file)
        key = os.getenv("OPENWEATHER_API_KEY")
        if key:
            return key

    # 3. Fallback: Clave embebida ofuscada
    return _get_obfuscated_key()

# Configuración Global
API_KEY = load_api_config()
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
