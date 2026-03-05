from utils.validator import validate_city_name

def test_validate_city_name_valid():
    assert validate_city_name("Tarija") is True
    assert validate_city_name("La Paz") is True
    assert validate_city_name("New York, US") is True
    assert validate_city_name("Ciudad de México") is True

def test_validate_city_name_invalid():
    assert validate_city_name("") is False
    assert validate_city_name("   ") is False
    assert validate_city_name("City123") is False
    assert validate_city_name("City@!") is False
