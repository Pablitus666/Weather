import os
import json
import locale
from .resources import locale_path

_translations = {}

def load_i18n():
    """Carga las traducciones según el idioma del sistema (soporte para 9 idiomas)."""
    global _translations
    try:
        # Obtener código de idioma (ej: 'es_ES' -> 'es')
        lang_code = locale.getdefaultlocale()[0]
        lang = lang_code.split('_')[0].lower() if lang_code else 'en'
    except Exception:
        lang = 'en'
    
    # Lista de idiomas soportados
    supported_langs = ["de", "en", "es", "fr", "it", "ja", "pt", "ru", "zh"]
    
    file = f"{lang}.json" if lang in supported_langs else "en.json"
    path = locale_path(file)
    
    if os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                _translations = json.load(f)
        except Exception:
            _translations = {}
    else:
        # Fallback a inglés si no existe el archivo específico
        path_en = locale_path("en.json")
        if os.path.exists(path_en):
            with open(path_en, 'r', encoding='utf-8') as f:
                _translations = json.load(f)

def _(key):
    """Obtiene la traducción para una clave dada."""
    return _translations.get(key, key)
