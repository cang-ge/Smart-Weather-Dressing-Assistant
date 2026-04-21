"""
Chinese Utility Module
=====================
Utilities for Chinese text processing, including pinyin conversion.
"""

from pypinyin import lazy_pinyin

# Foreign cities - Chinese to English mapping
FOREIGN_CITIES = {
    '伦敦': 'London',
    '巴黎': 'Paris',
    '柏林': 'Berlin',
    '东京': 'Tokyo',
    '纽约': 'New York',
    '洛杉矶': 'Los Angeles',
    '悉尼': 'Sydney',
    '首尔': 'Seoul',
    '曼谷': 'Bangkok',
    '新加坡': 'Singapore',
    '罗马': 'Rome',
    '米兰': 'Milan',
    '马德里': 'Madrid',
    '巴塞罗那': 'Barcelona',
    '阿姆斯特丹': 'Amsterdam',
    '苏黎世': 'Zurich',
    '维也纳': 'Vienna',
    '布拉格': 'Prague',
    '莫斯科': 'Moscow',
    '圣彼得堡': 'Saint Petersburg',
    '伊斯坦布尔': 'Istanbul',
    '迪拜': 'Dubai',
    '多哈': 'Doha',
    '孟买': 'Mumbai',
    '新德里': 'New Delhi',
    '雅加达': 'Jakarta',
    '吉隆坡': 'Kuala Lumpur',
    '马尼拉': 'Manila',
    '胡志明市': 'Ho Chi Minh City',
    '河内': 'Hanoi',
    '开罗': 'Cairo',
    '约翰内斯堡': 'Johannesburg',
    '开普敦': 'Cape Town',
    '里约热内卢': 'Rio de Janeiro',
    '布宜诺斯艾利斯': 'Buenos Aires',
    '墨西哥城': 'Mexico City',
    '温哥华': 'Vancouver',
    '多伦多': 'Toronto',
    '蒙特利尔': 'Montreal',
    '旧金山': 'San Francisco',
    '西雅图': 'Seattle',
    '波士顿': 'Boston',
    '芝加哥': 'Chicago',
    '华盛顿': 'Washington',
    '休斯顿': 'Houston',
    '迈阿密': 'Miami',
    '拉斯维加斯': 'Las Vegas',
    '夏威夷': 'Hawaii',
    '檀香山': 'Honolulu',
    '堪培拉': 'Canberra',
    '墨尔本': 'Melbourne',
    '布里斯班': 'Brisbane',
    '珀斯': 'Perth',
    '奥克兰': 'Auckland',
    '惠灵顿': 'Wellington',
}

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


def get_english_city_name(city: str) -> str:
    """
    Get English name for a Chinese city name.

    Args:
        city: Chinese city name (e.g., "伦敦", "东京")

    Returns:
        English city name or None if not found in FOREIGN_CITIES
    """
    return FOREIGN_CITIES.get(city)