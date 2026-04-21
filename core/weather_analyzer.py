"""
Weather Analyzer Module
======================
Analyzes and parses raw weather data into structured format.
"""

from typing import Dict, Optional

import sys
import os
sys.path.insert(0, str(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from utils.weather_codes import weather_code_to_text
from api.hefeng_api import HeFengWeatherProvider
from api.openmeteo_api import OpenMeteoWeatherProvider


def analyze_hefeng_weather(data: Dict) -> Dict:
    """
    Parse HeFeng weather API response.

    Args:
        data: Raw weather data from HeFeng API

    Returns:
        Structured weather info dict
    """
    result = {"source": "和风天气"}
    try:
        now = data.get("now", {})
        result["温度"] = f"{now.get('temp', 'N/A')}°C"
        result["体感温度"] = f"{now.get('feelsLike', 'N/A')}°C"
        result["天气状况"] = now.get('text', '未知')
        result["风速"] = f"{now.get('windSpeed', 'N/A')} km/h"
        result["风速等级"] = now.get('windScale', '未知')
        result["湿度"] = f"{now.get('humidity', 'N/A')}%"
        result["气压"] = f"{now.get('pressure', 'N/A')} hPa"
    except Exception as e:
        print(f"HeFeng解析失败: {e}")
    return result


def analyze_open_meteo_weather(data: Dict) -> Dict:
    """
    Parse Open-Meteo weather API response.

    Args:
        data: Raw weather data from Open-Meteo API

    Returns:
        Structured weather info dict
    """
    result = {"source": "Open-Meteo"}
    try:
        daily = data.get("daily", {})
        times = daily.get("time", [])
        if times:
            result["日期"] = times[0]
            result["最高温度"] = f"{daily['temperature_2m_max'][0]}°C"
            result["最低温度"] = f"{daily['temperature_2m_min'][0]}°C"
            result["温度"] = f"{daily['temperature_2m_min'][0]}~{daily['temperature_2m_max'][0]}°C"
            result["降水"] = f"{daily['precipitation_sum'][0]} mm"
            result["天气代码"] = daily['weathercode'][0]
            result["天气状况"] = weather_code_to_text(daily['weathercode'][0])
            result["未来几天"] = []

            for i in range(min(7, len(times))):
                result["未来几天"].append({
                    "日期": times[i],
                    "最高温": daily['temperature_2m_max'][i],
                    "最低温": daily['temperature_2m_min'][i],
                    "天气": weather_code_to_text(daily['weathercode'][i]),
                    "降水": daily['precipitation_sum'][i]
                })
    except Exception as e:
        print(f"Open-Meteo解析失败: {e}")
    return result


def analyze_weather(weather_data: Dict, source: str = "openmeteo") -> Dict:
    """
    Analyze weather data from any source.

    Args:
        weather_data: Raw weather data
        source: Data source ("hefeng" or "openmeteo")

    Returns:
        Structured weather info dict
    """
    if source == "hefeng":
        return analyze_hefeng_weather(weather_data)
    else:
        return analyze_open_meteo_weather(weather_data)


def get_weather_info(city_name: str, source: str = None) -> tuple[Optional[Dict], str]:
    """
    Get complete weather information for a city.

    Args:
        city_name: Name of the city
        source: Preferred weather source (None for auto-select)

    Returns:
        Tuple of (weather_info_dict, source_name)
    """
    weather_data = None
    selected_source = "openmeteo"  # default

    # Try HeFeng first if preferred or available
    if source == "hefeng" or source is None:
        hefeng = HeFengWeatherProvider()
        weather_data = hefeng.get_weather(city_name)
        if weather_data:
            selected_source = "hefeng"

    # Fallback to Open-Meteo
    if not weather_data:
        openmeteo = OpenMeteoWeatherProvider()
        weather_data = openmeteo.get_weather(city_name)
        if weather_data:
            selected_source = "openmeteo"

    if not weather_data:
        return None, selected_source

    weather_info = analyze_weather(weather_data, selected_source)
    return weather_info, selected_source