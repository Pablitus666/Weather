import re

def validate_city_name(name: str) -> bool:
    """Valida que el nombre de la ciudad solo contenga letras, espacios y comas."""
    if not name.strip():
        return False
    # Permitir letras, acentos, espacios y comas
    pattern = r"^[a-zA-ZñÑáéíóúÁÉÍÓÚ\s,]+$"
    return bool(re.match(pattern, name))
