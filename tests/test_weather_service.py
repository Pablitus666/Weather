import pytest
from services.weather_service import WeatherService
from core.exceptions import CityNotFoundError
from core.models import WeatherData

@pytest.mark.asyncio
async def test_get_weather_success(mocker):
    # Simular una respuesta exitosa de la API
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "name": "Tarija",
        "sys": {"country": "BO"},
        "main": {"temp": 25.5, "humidity": 40},
        "weather": [{"description": "cielo claro", "icon": "01d", "id": 800}],
        "wind": {"speed": 10.5}
    }
    
    # Mockear el cliente HTTP
    mock_client = mocker.patch("httpx.AsyncClient.get", return_value=mock_response)
    
    service = WeatherService()
    result = await service.get_weather("Tarija")
    
    assert isinstance(result, WeatherData)
    assert result.city == "Tarija"
    assert result.temperature == 25.5
    assert result.weather_id == 800

@pytest.mark.asyncio
async def test_get_weather_city_not_found(mocker):
    # Simular error 404
    mock_response = mocker.Mock()
    mock_response.status_code = 404
    
    mocker.patch("httpx.AsyncClient.get", return_value=mock_response)
    
    service = WeatherService()
    with pytest.raises(CityNotFoundError):
        await service.get_weather("CiudadInexistente123")
