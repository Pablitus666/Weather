from dataclasses import dataclass

@dataclass(frozen=True)
class WeatherData:
    """Modelo de datos inmutable para garantizar la integridad de la información."""
    city: str
    country: str
    temperature: float
    description: str
    icon_code: str
    weather_id: int
    humidity: int
    wind_speed: float
