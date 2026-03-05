import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# 1. Obtener la ruta base real del ejecutable para buscar el .env externo
# sys._MEIPASS es el directorio temporal de PyInstaller
# sys.executable es la ruta al .exe real
if getattr(sys, 'frozen', False):
    # Entorno ejecutable (.exe)
    base_path = Path(sys.executable).parent
else:
    # Entorno de desarrollo (.py)
    base_path = Path(__file__).resolve().parent.parent

# 2. Cargar variables del entorno del sistema y archivo .env externo
# Priorizamos el entorno del sistema, luego el .env local en la carpeta del ejecutable
load_dotenv()
env_path = base_path / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)

# 3. Obtener la API_KEY
API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# NOTA: No lanzamos RuntimeError aquí para permitir que la UI se inicie y 
# pueda mostrar un mensaje de error amigable al usuario si falta la clave.
if not API_KEY:
    # Registramos una advertencia en lugar de romper la app
    print("WARNING: OPENWEATHER_API_KEY no encontrada.")
