import json
import os
import platform
from pathlib import Path

class SettingsManager:
    """
    Gestiona la configuración persistente multi-plataforma.
    """
    def __init__(self):
        self.app_name = "WeatherReportPro"
        self.config_dir = self._get_config_dir()
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.config_file = self.config_dir / "settings.json"
        
        self.defaults = {
            "last_city": "",
            "units": "metric",
            "lang": "es",
            "theme": "dark"
        }
        self.settings = self.load_settings()

    def _get_config_dir(self):
        """Retorna la ruta de configuración estándar del SO."""
        if platform.system() == "Windows":
            return Path(os.getenv('APPDATA')) / self.app_name
        elif platform.system() == "Darwin":
            return Path.home() / "Library/Application Support" / self.app_name
        else:
            return Path.home() / ".config" / self.app_name

    def load_settings(self):
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return {**self.defaults, **json.load(f)}
            except Exception:
                return self.defaults
        return self.defaults

    def save_settings(self):
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=4)
        except Exception:
            pass

    def get(self, key):
        return self.settings.get(key, self.defaults.get(key))

    def set(self, key, value):
        self.settings[key] = value
        self.save_settings()
