import os
from dotenv import load_dotenv

# 1. Cargar variables del entorno del sistema (Prioridad Producción)
load_dotenv()

# 2. Fallback: Cargar archivo .env local solo si existe (Prioridad Desarrollo)
# Nota: En producción, las credenciales deben inyectarse en el entorno, no en archivos.
if os.path.exists(".env"):
    load_dotenv(".env")

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# Validación estricta
if not API_KEY:
    # Mensaje profesional para logs de crash
    raise RuntimeError(
        "CRITICAL: OPENWEATHER_API_KEY no configurada. "
        "Asegúrese de establecer la variable de entorno o incluir un archivo .env en el directorio de ejecución."
    )
