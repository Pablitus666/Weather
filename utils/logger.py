import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import os
import platform
import sys

APP_NAME = "WeatherReportPro"

def get_log_dir():
    """Determina la ruta de logs según el estándar del SO."""
    if platform.system() == "Windows":
        base = Path(os.getenv("APPDATA"))
    elif platform.system() == "Darwin": # macOS
        base = Path.home() / "Library/Application Support"
    else: # Linux
        base = Path.home() / ".config"

    log_dir = base / APP_NAME / "logs"
    try:
        log_dir.mkdir(parents=True, exist_ok=True)
    except Exception:
        # Fallback local si no hay permisos
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
    return log_dir

log_file = get_log_dir() / "weather.log"

# Handler rotativo: Máx 2MB, mantiene 3 copias de respaldo
handler = RotatingFileHandler(
    log_file,
    maxBytes=2_000_000,
    backupCount=3,
    encoding="utf-8"
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    handlers=[
        handler,
        logging.StreamHandler(sys.stdout) # También a consola para dev
    ]
)

logger = logging.getLogger(APP_NAME)
