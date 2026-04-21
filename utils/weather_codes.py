"""
Weather Code Mapping Module
===========================
WMO (World Meteorological Organization) weather code to Chinese text mapping.
"""

# WMO Weather Interpretation Codes
# Reference: https://open-meteo.com/en/docs#weathers

WMO_WEATHER_CODES = {
    0: "晴",
    1: "晴间多云",
    2: "多云",
    3: "阴",
    45: "雾",
    48: "霜雾",
    51: "小毛毛雨",
    53: "中毛毛雨",
    55: "大毛毛雨",
    56: "冻毛毛雨",
    57: "强冻毛毛雨",
    61: "小雨",
    63: "中雨",
    65: "大雨",
    66: "冻雨",
    67: "强冻雨",
    71: "小雪",
    73: "中雪",
    75: "大雪",
    77: "雪粒",
    80: "小阵雨",
    81: "中阵雨",
    82: "大阵雨",
    85: "小阵雪",
    86: "大阵雪",
    95: "雷暴",
    96: "雷暴+小冰雹",
    99: "雷暴+大冰雹",
}


def weather_code_to_text(code: int) -> str:
    """
    Convert WMO weather code to Chinese text.

    Args:
        code: WMO weather code (integer)

    Returns:
        Chinese description of the weather
    """
    return WMO_WEATHER_CODES.get(code, f"未知({code})")


def get_weather_emoji(code: int) -> str:
    """
    Get emoji for weather code.

    Args:
        code: WMO weather code

    Returns:
        Emoji representation of weather
    """
    emoji_map = {
        0: "☀️",    # sunny
        1: "🌤️",    # partly cloudy
        2: "⛅",    # cloudy
        3: "☁️",    # overcast
        45: "🌫️",   # fog
        48: "🌫️",   # freezing fog
        51: "🌧️",   # drizzle
        61: "🌧️",   # rain
        63: "🌧️",   # moderate rain
        65: "🌧️",   # heavy rain
        71: "🌨️",   # snow
        73: "🌨️",   # moderate snow
        75: "❄️",   # heavy snow
        80: "🌦️",   # rain showers
        95: "⛈️",   # thunderstorm
    }
    return emoji_map.get(code, "🌤️")