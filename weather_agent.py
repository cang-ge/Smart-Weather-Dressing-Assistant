"""
智能天气穿搭助手 - CLI入口
===========================
命令行天气查询和穿搭建议工具

Usage:
    python weather_agent.py [city_name]

Example:
    python weather_agent.py 北京
    python weather_agent.py Shanghai
"""

import os
import sys

# Add project root to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Core modules
from core import get_weather_info, get_outfit_suggestion
from visualization import draw_weather_trend

# Suppress SSL warnings
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def query_weather(city: str) -> None:
    """
    Query weather and display results for a city.

    Args:
        city: City name
    """
    if not city:
        print("错误: 请输入城市名称")
        print("用法: python weather_agent.py [城市名称]")
        return

    print("=" * 50)
    print(f"  正在查询 {city} 的天气信息...")
    print("=" * 50)

    # Get weather data
    weather_info, source = get_weather_info(city)

    if not weather_info:
        print(f"\n❌ 无法获取 {city} 的天气数据")
        print("   可能的原因:")
        print("   - 城市名称不正确")
        print("   - 网络连接问题")
        print("   - API服务暂时不可用")
        return

    # Display weather info
    print(f"\n📍 {city} 天气详情")
    print(f"   数据来源: {weather_info.get('source', '未知')}")
    print(f"   当前天气: {weather_info.get('天气状况', '未知')}")
    print(f"   温度: {weather_info.get('温度', '未知')}")
    print(f"   降水: {weather_info.get('降水', '未知')}")

    # Display forecast
    if "未来几天" in weather_info:
        print("\n📅 未来一周预报:")
        for day in weather_info["未来几天"]:
            date_str = day["日期"][-5:]
            print(f"   {date_str}: {day['天气']} {day['最低温']}~{day['最高温']}°C 降水:{day['降水']}mm")

    # Get outfit suggestion
    print("\n" + "=" * 50)
    print("👗 穿搭建议")
    print("=" * 50)
    outfit = get_outfit_suggestion(weather_info, source)
    print(outfit)

    # Generate chart
    if "未来几天" in weather_info:
        print("\n" + "=" * 50)
        print("📊 正在生成天气趋势图...")
        print("=" * 50)
        save_path = os.path.join(os.getcwd(), f"{city}_weather_trend.png")
        fig = draw_weather_trend(weather_info, city, save_path)
        if fig:
            print(f"✅ 图表已保存: {save_path}")

    print("\n✨ 查询完成！")


def main():
    """Main CLI entry point."""
    print("=" * 50)
    print("  🌤️  Weather Outfit Assistant  🌤️")
    print("=" * 50)

    # Get city from command line argument
    if len(sys.argv) > 1:
        city = " ".join(sys.argv[1:])  # Handle multi-word city names
    else:
        city = input("\n请输入城市名称（如：北京、上海、广州）: ").strip()

    query_weather(city)


if __name__ == "__main__":
    main()