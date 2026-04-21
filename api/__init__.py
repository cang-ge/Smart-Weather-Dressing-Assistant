"""Weather Outfit Assistant - API Package"""

from .weather_base import WeatherProvider
from .hefeng_api import HeFengWeatherProvider, get_hefeng_weather
from .openmeteo_api import OpenMeteoWeatherProvider, get_open_meteo_weather

__all__ = [
    'WeatherProvider',
    'HeFengWeatherProvider',
    'get_hefeng_weather',
    'OpenMeteoWeatherProvider',
    'get_open_meteo_weather',
]