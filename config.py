"""
Weather Outfit Assistant - Configuration Module
================================================
Centralized configuration management for API keys, URLs, and constants.
"""

import os
from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).parent

# ============== API Configuration ==============

# HeFeng Weather API (requires registration: https://dev.heweather.com/)
# Set via environment variable HEFENG_API_KEY or modify below
HEFENG_API_KEY = os.environ.get("HEFENG_API_KEY", "API_KEY_HERE")

# Open-Meteo API (free, no API key required)
OPEN_METEO_BASE_URL = "https://api.open-meteo.com/v1/forecast"
GEOCODING_API_URL = "https://geocoding-api.open-meteo.com/v1/search"

# ============== Weather Data Settings ==============

DEFAULT_FORECAST_DAYS = 7
REQUEST_TIMEOUT = 30  # seconds

# ============== Visualization Settings ==============

CHART_DPI = 150
CHART_FIGSIZE = (10, 8)

# Matplotlib Chinese font configuration
MATPLOTLIB_FONT_CONFIGURED = False

def configure_matplotlib():
    """Configure matplotlib for Chinese font support"""
    global MATPLOTLIB_FONT_CONFIGURED
    if MATPLOTLIB_FONT_CONFIGURED:
        return

    import matplotlib.pyplot as plt
    import matplotlib
    matplotlib.use('Agg')
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
    MATPLOTLIB_FONT_CONFIGURED = True

# ============== Outfit Suggestion Temperature Ranges ==============

TEMP_RANGES = {
    "freezing": (None, 0),      # < 0°C
    "cold": (0, 10),            # 0-10°C
    "cool": (10, 15),           # 10-15°C
    "comfortable": (15, 20),    # 15-20°C
    "warm": (20, 25),           # 20-25°C
    "hot": (25, 30),            # 25-30°C
    "very_hot": (30, None),     # >= 30°C
}