import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# 1. API KEY EMBEBIDA POR DEFECTO (Portabilidad Total)
# Esta clave se incluye directamente en el ejecutable para que funcione "Out of the box".
DEFAULT_API_KEY = "6d16d24abaebaee9557ff6d2d37e903b"

# 2. Obtener la ruta base real para buscar posibles sobrescrituras externas
if getattr(sys, 'frozen', False):
    base_path = Path(sys.executable).parent
else:
    base_path = Path(__file__).resolve().parent.parent

# 3. Carga de variables del sistema y archivo .env externo (Opcional)
load_dotenv()
env_path = base_path / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)

# 4. Prioridad: Entorno del Sistema > Archivo .env externo > Clave Embebida
API_KEY = os.getenv("OPENWEATHER_API_KEY") or DEFAULT_API_KEY
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
