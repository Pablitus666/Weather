# Configuración Visual (Consistencia de Marca)
COLOR_BG = '#023047'
COLOR_ACCENT = '#219ebc'
COLOR_TEXT = '#ffffff'
COLOR_HOVER = '#fcbf49'

# Tipografías
FONT_TITLE = ("Arial", 20, "bold")
FONT_TEMP = ("Arial", 60, "bold")
FONT_INFO = ("Comic Sans MS", 14, "bold")
FONT_BUTTON = ("Comic Sans MS", 12, "bold")

# Rutas de Imágenes
IMAGE_LOGO_ICO = "assets/images/loguito.ico"
IMAGE_LOGO_PNG = "assets/images/logo.png"
IMAGE_ROBOT = "assets/images/robot.png"
IMAGE_BOTON = "assets/images/boton.png"

# Información de Aplicación
APP_VERSION = "1.0.0"

# Mapeo de códigos OpenWeather a nombres de archivo amigables
# Esto permite que si el usuario tiene 'clear.png', 'clouds.png', etc., se carguen automáticamente.
WEATHER_ICON_MAP = {
    "01": "clear",       # Cielo despejado
    "02": "few_clouds",  # Algunas nubes
    "03": "clouds",      # Nubes dispersas
    "04": "clouds",      # Nublado
    "09": "lightrain",   # Llovizna / Lluvia ligera
    "10": "heavyrain",   # Lluvia fuerte
    "11": "storm",       # Tormenta
    "13": "snow",        # Nieve
    "50": "mist"         # Niebla/Bruma
}
