"""
Chinese Utility Module
=====================
Utilities for Chinese text processing, including pinyin conversion.
"""

from pypinyin import lazy_pinyin

def convert_chinese_to_pinyin(city_name: str) -> str:
    """
    Convert Chinese city name to pinyin for API queries.

    Args:
        city_name: Chinese city name (e.g., "北京", "上海")

    Returns:
        Pinyin string (e.g., "beijing", "shanghai")
    """
    pinyin_list = lazy_pinyin(city_name)
    return ''.join(pinyin_list)


def is_chinese(text: str) -> bool:
    """
    Check if text contains any Chinese characters.

    Args:
        text: Input string to check

    Returns:
        True if text contains Chinese characters, False otherwise
    """
    return any('\u4e00' <= char <= '\u9fff' for char in text)