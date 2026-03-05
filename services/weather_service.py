import httpx
import time
from app.config import API_KEY, BASE_URL
from core.models import WeatherData
from core.exceptions import WeatherError, CityNotFoundError, APIError, NetworkError
from utils.logger import logger

class WeatherService:
    """
    Servicio de clima Enterprise-Grade.
    - Cliente HTTP persistente (Connection Pooling).
    - Manejo de Rate Limiting (429).
    - Caché en memoria.
    """
    def __init__(self):
        self.params = {
            "APPID": API_KEY,
            "units": "metric",
            "lang": "es"
        }
        # Cliente persistente para reutilizar conexiones TCP (Mejor rendimiento)
        self.client = httpx.AsyncClient(
            timeout=10.0,
            limits=httpx.Limits(
                max_keepalive_connections=5, 
                max_connections=10
            )
        )
        self._cache = {}
        self.CACHE_TTL = 600

    async def get_weather(self, city_name: str) -> WeatherData:
        city_key = city_name.lower().strip()
        
        # 1. Caché
        if city_key in self._cache:
            data, timestamp = self._cache[city_key]
            if time.time() - timestamp < self.CACHE_TTL:
                logger.info(f"Caché HIT para: {city_name}")
                return data

        # 2. Red
        try:
            logger.info(f"Consultando red para: {city_name}")
            params = self.params.copy()
            params["q"] = city_name
            
            # Usamos el cliente persistente
            response = await self.client.get(BASE_URL, params=params)
            
            if response.status_code == 404:
                raise CityNotFoundError(f"Ciudad no encontrada: {city_name}")
            elif response.status_code == 401:
                raise APIError("Credenciales de API inválidas.")
            elif response.status_code == 429:
                logger.warning("Rate Limit Exceeded (429)")
                raise APIError("Límite de peticiones excedido. Intente más tarde.")
            
            response.raise_for_status()
            data_json = response.json()
            
            weather = WeatherData(
                city=data_json["name"],
                country=data_json["sys"]["country"],
                temperature=data_json["main"]["temp"],
                description=data_json["weather"][0]["description"].capitalize(),
                icon_code=data_json["weather"][0]["icon"],
                weather_id=data_json["weather"][0]["id"],
                humidity=data_json["main"]["humidity"],
                wind_speed=data_json["wind"]["speed"]
            )
            
            self._cache[city_key] = (weather, time.time())
            return weather

        except WeatherError:
            raise
        except (httpx.RequestError, httpx.HTTPStatusError) as e:
            logger.error(f"Fallo de comunicación: {type(e).__name__} - {str(e)}")
            raise NetworkError("Fallo de conexión.")
        except Exception as e:
            logger.exception(f"Fallo técnico crítico: {e}")
            raise

    async def close(self):
        """Cierra limpiamente el cliente HTTP y libera recursos."""
        await self.client.aclose()
        logger.info("WeatherService: Cliente HTTP cerrado.")
