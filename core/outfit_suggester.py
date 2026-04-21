"""
Outfit Suggester Module
=======================
Generates outfit suggestions based on weather conditions.
"""

from typing import Dict

import sys
import os
sys.path.insert(0, str(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from config import TEMP_RANGES


def generate_outfit_text(temp: int, feels_like: int, condition: str) -> str:
    """
    Generate outfit suggestion text based on temperature and conditions.

    Args:
        temp: Temperature in Celsius
        feels_like: Feels like temperature in Celsius
        condition: Weather condition description

    Returns:
        Formatted outfit suggestion string
    """
    suggestions = []

    # Determine temperature range
    if temp < 0:
        suggestions.append("❄️ [FREEZING] 严寒天气（<0°C）")
        suggestions.append("• 羽绒服/厚棉服 + 保暖内衣")
        suggestions.append("• 围巾 + 手套 + 帽子")
        suggestions.append("• 雪地靴或厚棉鞋")
    elif temp < 10:
        suggestions.append("🥶 [COLD] 寒冷天气（0-10°C）")
        suggestions.append("• 棉衣/轻薄羽绒服 + 毛衣/卫衣")
        suggestions.append("• 牛仔裤/保暖裤")
        suggestions.append("• 围巾（防风）")
    elif temp < 15:
        suggestions.append("🧥 [COOL] 凉意天气（10-15°C）")
        suggestions.append("• 薄外套/夹克 + 衬衫/T恤")
        suggestions.append("• 长裤/休闲裤")
        suggestions.append("• 早晚建议加件薄针织衫")
    elif temp < 20:
        suggestions.append("👕 [COMFORTABLE] 舒适天气（15-20°C）")
        suggestions.append("• 薄长袖 + 休闲外套")
        suggestions.append("• 牛仔裤/休闲裤")
        suggestions.append("• 单鞋或运动鞋")
    elif temp < 25:
        suggestions.append("☀️ [WARM] 温暖天气（20-25°C）")
        suggestions.append("• T恤/衬衫 + 薄外套（备用）")
        suggestions.append("• 牛仔裤/长裙")
        suggestions.append("• 舒适运动鞋")
    elif temp < 30:
        suggestions.append("🔥 [HOT] 炎热天气（25-30°C）")
        suggestions.append("• 短袖 + 轻薄长裤")
        suggestions.append("• 遮阳帽/太阳镜")
        suggestions.append("• 透气运动鞋")
    else:
        suggestions.append("⚠️ [VERY HOT] 高温天气（>30°C）")
        suggestions.append("• 透气短袖/背心")
        suggestions.append("• 短裤/轻薄长裤")
        suggestions.append("• 防晒 + 充足补水")

    # Weather-specific suggestions
    if "雨" in condition or "雪" in condition:
        suggestions.append("")
        suggestions.append("🌧️ [RAIN] 雨雪天气提示:")
        suggestions.append("• 请携带雨伞/雨衣")
        suggestions.append("• 穿防滑鞋，避免滑倒")
        if temp < 15:
            suggestions.append("• 建议穿防水外套")

    if "雾" in condition or "霾" in condition:
        suggestions.append("")
        suggestions.append("🌫️ [FOG] 雾霾天气提示:")
        suggestions.append("• 佩戴口罩")
        suggestions.append("• 穿亮色系衣服便于识别")
        suggestions.append("• 驾车请注意安全")

    if "晴" in condition and temp > 25:
        suggestions.append("")
        suggestions.append("☀️ [SUNNY] 晴天防晒提示:")
        suggestions.append("• 涂抹防晒霜")
        suggestions.append("• 戴遮阳帽或撑伞")

    return "\n".join(suggestions)


def get_outfit_hefeng(weather: Dict) -> str:
    """
    Generate outfit suggestion from HeFeng weather data.

    Args:
        weather: Weather info dict from HeFeng

    Returns:
        Outfit suggestion string
    """
    temp_str = weather.get("温度", "0°C").replace("°C", "").replace("C", "")
    try:
        temp = int(temp_str)
    except:
        temp = 20

    condition = weather.get("天气状况", "")
    feels_like_str = weather.get("体感温度", "0°C").replace("°C", "").replace("C", "")
    try:
        feels_like = int(feels_like_str)
    except:
        feels_like = temp

    return generate_outfit_text(temp, feels_like, condition)


def get_outfit_open_meteo(weather: Dict) -> str:
    """
    Generate outfit suggestion from Open-Meteo weather data.

    Args:
        weather: Weather info dict from Open-Meteo

    Returns:
        Outfit suggestion string
    """
    temp_str = weather.get("温度", "20°C").replace("°C", "").replace("C", "")
    try:
        if "~" in temp_str:
            parts = temp_str.split("~")
            temp = (int(parts[0]) + int(parts[1])) // 2
        else:
            temp = int(temp_str)
    except:
        temp = 20

    condition = weather.get("天气状况", "")
    return generate_outfit_text(temp, temp, condition)


def get_outfit_suggestion(weather_info: Dict, source: str = "openmeteo") -> str:
    """
    Generate outfit suggestion based on weather info.

    Args:
        weather_info: Structured weather info dict
        source: Weather data source ("hefeng" or "openmeteo")

    Returns:
        Formatted outfit suggestion string
    """
    if source == "hefeng":
        return get_outfit_hefeng(weather_info)
    else:
        return get_outfit_open_meteo(weather_info)