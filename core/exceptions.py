class WeatherError(Exception):
    """Clase base para errores de clima."""
    pass

class CityNotFoundError(WeatherError):
    """Se lanza cuando la ciudad no existe en OpenWeather."""
    pass

class APIError(WeatherError):
    """Se lanza cuando hay un problema con la API Key o límites."""
    pass

class NetworkError(WeatherError):
    """Se lanza cuando no hay conexión a internet."""
    pass
