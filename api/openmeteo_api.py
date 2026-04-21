"""
Open-Meteo API Module
====================
Weather data provider using Open-Meteo API (free, no API key required).
"""

import requests
from typing import Optional, Dict
from .weather_base import WeatherProvider

import sys
import os
sys.path.insert(0, str(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from config import OPEN_METEO_BASE_URL, REQUEST_TIMEOUT
from utils.chinese_util import convert_chinese_to_pinyin, is_chinese, get_english_city_name


class OpenMeteoWeatherProvider(WeatherProvider):
    """Open-Meteo API provider (free, no API key required)."""

    def get_provider_name(self) -> str:
        return "Open-Meteo"

    def _fetch_weather(self, name: str) -> Optional[Dict]:
        """
        Internal method to fetch weather by city name.

        Args:
            name: City name to search

        Returns:
            Weather data dict or None if not found
        """
        geo_resp = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": name, "count": 1},
            timeout=REQUEST_TIMEOUT,
            verify=False
        )
        geo_data = geo_resp.json()
        if not geo_data.get("results"):
            return None

        lat = geo_data["results"][0]["latitude"]
        lon = geo_data["results"][0]["longitude"]
        timezone = geo_data["results"][0].get("timezone", "Asia/Shanghai")

        weather_url = (
            f"{OPEN_METEO_BASE_URL}"
            f"?latitude={lat}&longitude={lon}&timezone={timezone}"
            f"&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,weathercode"
            f"&forecast_days=7"
        )
        weather_resp = requests.get(weather_url, timeout=REQUEST_TIMEOUT, verify=False)
        return weather_resp.json()

    def get_weather(self, city_name: str) -> Optional[Dict]:
        """
        Fetch weather from Open-Meteo API.
        Automatically converts Chinese city names to pinyin or English.

        Args:
            city_name: Name of the city (supports Chinese and English)

        Returns:
            Weather data dict or None if failed
        """
        try:
            # Try direct query first
            result = self._fetch_weather(city_name)
            if result:
                return result

            # If failed and contains Chinese, try conversion
            if is_chinese(city_name):
                # 1. Try foreign cities mapping (e.g., 伦敦 -> London)
                en_name = get_english_city_name(city_name)
                if en_name:
                    result = self._fetch_weather(en_name)
                    if result:
                        return result

                # 2. Try pinyin conversion (e.g., 北京 -> beijing)
                pinyin_name = convert_chinese_to_pinyin(city_name)
                result = self._fetch_weather(pinyin_name)
                if result:
                    return result

            return None
        except Exception as e:
            print(f"Open-Meteo查询失败: {e}")
            return None


def get_open_meteo_weather(city_name: str) -> Optional[Dict]:
    """
    Convenience function to get Open-Meteo weather.

    Args:
        city_name: Name of the city

    Returns:
        Weather data dict or None if failed
    """
    provider = OpenMeteoWeatherProvider()
    return provider.get_weather(city_name)