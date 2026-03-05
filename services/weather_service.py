import httpx
import time
import json
import os
from app.config import API_KEY, BASE_URL, get_base_path
from core.models import WeatherData
from core.exceptions import WeatherError, CityNotFoundError, APIError, NetworkError
from utils.logger import logger

class WeatherService:
    """
    Servicio de clima Nivel Elite.
    - Timeout optimizado (8s).
    - Caché persistente en disco (10 min).
    - Validación robusta de JSON y Red.
    """
    def __init__(self):
        # Cargamos API_KEY de forma dinámica
        from app.config import API_KEY
        self.params = {
            "APPID": API_KEY,
            "units": "metric",
            "lang": "es"
        }
        # Mejora 1: Timeout de red optimizado a 8.0s
        self.client = httpx.AsyncClient(
            timeout=8.0,
            limits=httpx.Limits(max_keepalive_connections=5, max_connections=10)
        )
        
        # Mejora 3: Caché local persistente (Nivel Profesional)
        self.cache_file = get_base_path() / "weather_cache.json"
        self._cache = self._load_cache()
        self.CACHE_TTL = 600 # 10 minutos

    def _load_cache(self):
        """Carga el caché desde el disco si existe."""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def _save_cache(self):
        """Persiste el caché en el disco."""
        try:
            with open(self.cache_file, "w", encoding="utf-8") as f:
                json.dump(self._cache, f, ensure_ascii=False, indent=4)
        except Exception as e:
            logger.error(f"Error guardando caché: {e}")

    async def get_weather(self, city_name: str) -> WeatherData:
        city_key = city_name.lower().strip()
        
        # 1. Verificar Caché (Memoria/Disco)
        if city_key in self._cache:
            entry = self._cache[city_key]
            if time.time() - entry["timestamp"] < self.CACHE_TTL:
                logger.info(f"Caché HIT (Elite) para: {city_name}")
                return WeatherData(**entry["data"])

        # 2. Consulta de Red
        try:
            from app.config import API_KEY
            params = self.params.copy()
            params["APPID"] = API_KEY
            params["q"] = city_name
            
            response = await self.client.get(BASE_URL, params=params)
            
            # Mejora 2: Manejo de error de red y HTTP
            if response.status_code == 401:
                raise APIError("error.api_invalid")
            elif response.status_code == 404:
                raise CityNotFoundError(f"Ciudad no encontrada: {city_name}")
            elif response.status_code == 429:
                raise APIError("error.rate_limit")
            elif response.status_code >= 500:
                raise APIError("error.server")
            
            response.raise_for_status()

            # Mejora 4: Validación de JSON robusta
            try:
                data_json = response.json()
            except Exception:
                logger.error("Respuesta inválida (No JSON) del servidor.")
                raise APIError("error.invalid_response")

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
            
            # Guardar en Caché Persistente
            self._cache[city_key] = {
                "timestamp": time.time(),
                "data": weather.__dict__
            }
            self._save_cache()
            
            return weather

        except (httpx.ConnectError, httpx.NetworkError):
            logger.error("Sin conexión a Internet.")
            raise NetworkError("error.no_internet")
        except (httpx.TimeoutException, httpx.ReadTimeout):
            logger.error("El servidor tardó demasiado en responder.")
            raise NetworkError("error.timeout")
        except WeatherError:
            raise
        except Exception as e:
            logger.exception(f"Fallo técnico: {e}")
            raise

    async def close(self):
        await self.client.aclose()
