"""
HeFeng Weather API Module
========================
Weather data provider using HeFeng Weather API.
"""

import requests
from typing import Optional, Dict
from .weather_base import WeatherProvider
import sys
import os

# Add parent directory to path for config import
sys.path.insert(0, str(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from config import HEFENG_API_KEY, REQUEST_TIMEOUT


class HeFengWeatherProvider(WeatherProvider):
    """HeFeng Weather API provider."""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or HEFENG_API_KEY

    def get_provider_name(self) -> str:
        return "和风天气"

    def get_location_id(self, city_name: str) -> Optional[str]:
        """
        Get city ID from HeFeng geocoding API.

        Args:
            city_name: Name of the city

        Returns:
            City ID string or None if not found
        """
        if not self.api_key or self.api_key == "API_KEY_HERE":
            return None

        url = f"https://geoapi.heweather.com/v2/city/lookup?name={city_name}&key={self.api_key}"
        try:
            resp = requests.get(url, timeout=REQUEST_TIMEOUT)
            data = resp.json()
            if data.get("code") == "200" and data.get("location"):
                return data["location"][0]["id"]
        except Exception as e:
            print(f"HeFeng城市查询失败: {e}")
        return None

    def get_weather(self, city_name: str) -> Optional[Dict]:
        """
        Fetch weather forecast from HeFeng API.

        Args:
            city_name: Name of the city

        Returns:
            Weather data dict or None if failed
        """
        if not self.api_key or self.api_key == "API_KEY_HERE":
            return None

        location_id = self.get_location_id(city_name)
        if not location_id:
            return None

        url = f"https://dev.heweather.com/v7/weather/7d?location={location_id}&key={self.api_key}"
        try:
            resp = requests.get(url, timeout=REQUEST_TIMEOUT)
            return resp.json()
        except Exception as e:
            print(f"HeFeng天气预报查询失败: {e}")
        return None


def get_hefeng_weather(city_name: str, days: int = 7) -> Optional[Dict]:
    """
    Convenience function to get HeFeng weather.

    Args:
        city_name: Name of the city
        days: Number of forecast days (default: 7)

    Returns:
        Weather data dict or None if failed
    """
    provider = HeFengWeatherProvider()
    return provider.get_weather(city_name)