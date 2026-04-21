"""
Weather API Base Module
=======================
Abstract base class for weather data providers.
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict


class WeatherProvider(ABC):
    """Abstract base class for weather data providers."""

    @abstractmethod
    def get_weather(self, city_name: str) -> Optional[Dict]:
        """
        Fetch weather data for a city.

        Args:
            city_name: Name of the city

        Returns:
            Raw weather data dict or None if failed
        """
        pass

    @abstractmethod
    def get_provider_name(self) -> str:
        """Return the name of this weather provider."""
        pass