"""
Chart Generator Module
=====================
Generates weather trend charts and visualizations.
"""

import matplotlib.pyplot as plt
from typing import Dict, List

import sys
import os
sys.path.insert(0, str(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from config import configure_matplotlib, CHART_DPI, CHART_FIGSIZE


def generate_temperature_chart(
    dates: List[str],
    max_temps: List[float],
    min_temps: List[float],
    city_name: str,
    save_path: str = None
) -> plt.Figure:
    """
    Generate temperature trend chart.

    Args:
        dates: List of date strings
        max_temps: List of maximum temperatures
        min_temps: List of minimum temperatures
        city_name: Name of the city
        save_path: Optional path to save the chart

    Returns:
        matplotlib Figure object
    """
    configure_matplotlib()

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(dates, max_temps, 'r-o', label='最高温', linewidth=2, markersize=8)
    ax.plot(dates, min_temps, 'b-o', label='最低温', linewidth=2, markersize=8)
    ax.fill_between(dates, min_temps, max_temps, alpha=0.3, color='orange')

    ax.set_xlabel('日期', fontsize=12)
    ax.set_ylabel('温度 (°C)', fontsize=12)
    ax.set_title(f'{city_name} 7天温度趋势', fontsize=14, fontweight='bold')
    ax.legend(loc='upper right')
    ax.grid(True, linestyle='--', alpha=0.7)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=CHART_DPI, bbox_inches='tight')

    return fig


def generate_precipitation_chart(
    dates: List[str],
    precipitation: List[float],
    city_name: str,
    save_path: str = None
) -> plt.Figure:
    """
    Generate precipitation forecast chart.

    Args:
        dates: List of date strings
        precipitation: List of precipitation values
        city_name: Name of the city
        save_path: Optional path to save the chart

    Returns:
        matplotlib Figure object
    """
    configure_matplotlib()

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.bar(dates, precipitation, color='steelblue', alpha=0.8)
    ax.set_xlabel('日期', fontsize=12)
    ax.set_ylabel('降水量 (mm)', fontsize=12)
    ax.set_title(f'{city_name} 7天降水预报', fontsize=14, fontweight='bold')
    ax.grid(True, linestyle='--', alpha=0.7, axis='y')

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=CHART_DPI, bbox_inches='tight')

    return fig


def generate_weather_dashboard(
    weather_info: Dict,
    city_name: str,
    save_path: str = None
) -> plt.Figure:
    """
    Generate a complete weather dashboard with temperature and precipitation.

    Args:
        weather_info: Structured weather info dict (must contain "未来几天" key)
        city_name: Name of the city
        save_path: Optional path to save the chart

    Returns:
        matplotlib Figure object
    """
    configure_matplotlib()

    if "未来几天" not in weather_info:
        print("没有足够数据绘制趋势图")
        return None

    days = weather_info["未来几天"]
    dates = [d["日期"][-5:] for d in days]
    max_temps = [d["最高温"] for d in days]
    min_temps = [d["最低温"] for d in days]
    precipitation = [d["降水"] for d in days]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=CHART_FIGSIZE)

    # Temperature chart
    ax1.plot(dates, max_temps, 'r-o', label='最高温', linewidth=2, markersize=8)
    ax1.plot(dates, min_temps, 'b-o', label='最低温', linewidth=2, markersize=8)
    ax1.fill_between(dates, min_temps, max_temps, alpha=0.3, color='orange')
    ax1.set_xlabel('日期', fontsize=12)
    ax1.set_ylabel('温度 (°C)', fontsize=12)
    ax1.set_title(f'{city_name} 7天温度趋势', fontsize=14, fontweight='bold')
    ax1.legend(loc='upper right')
    ax1.grid(True, linestyle='--', alpha=0.7)

    # Precipitation chart
    ax2.bar(dates, precipitation, color='steelblue', alpha=0.8)
    ax2.set_xlabel('日期', fontsize=12)
    ax2.set_ylabel('降水量 (mm)', fontsize=12)
    ax2.set_title(f'{city_name} 7天降水预报', fontsize=14, fontweight='bold')
    ax2.grid(True, linestyle='--', alpha=0.7, axis='y')

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=CHART_DPI, bbox_inches='tight')
        print(f"图表已保存: {save_path}")

    return fig


def draw_weather_trend(weather_info: Dict, city_name: str, save_path: str = None) -> plt.Figure:
    """
    Convenience function to draw weather trend chart.

    Args:
        weather_info: Structured weather info dict
        city_name: Name of the city
        save_path: Optional path to save the chart

    Returns:
        matplotlib Figure object or None
    """
    return generate_weather_dashboard(weather_info, city_name, save_path)