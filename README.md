# 🌤️ Weather Outfit Assistant - 智能天气穿搭助手

> 输入城市名称，获取实时天气预报和智能穿搭建议

[English](#english) | 简体中文

---

<a name="english"></a>

## 📌 Features

- **🌡️ Multi-source Weather Data**: Supports HeFeng Weather (paid API) and Open-Meteo (free, no API key)
- **👗 Smart Outfit Suggestions**: Professional clothing recommendations based on temperature, feels-like, and weather conditions
- **📊 7-Day Forecast Charts**: Auto-generated temperature trend and precipitation visualization
- **🌍 Global City Support**: Supports both Chinese and English city names, with automatic pinyin conversion for overseas cities
- **💬 Natural Language Queries**: Supports various query formats like "北京天气", "东京天气怎么样"
- **🌐 Beautiful Web Interface**: Feature-rich web client with quick city buttons

---

## 🏗️ Project Architecture

```
weather_agent/
├── config.py                 # Configuration (API keys, URLs, constants)
├── utils/                    # Utility modules
│   ├── __init__.py
│   ├── chinese_util.py       # Chinese text processing (pinyin conversion)
│   └── weather_codes.py      # WMO weather code mapping
├── api/                      # Weather API layer
│   ├── __init__.py
│   ├── weather_base.py       # Abstract base class for weather providers
│   ├── hefeng_api.py         # HeFeng Weather API implementation
│   └── openmeteo_api.py      # Open-Meteo API implementation
├── core/                     # Core business logic
│   ├── __init__.py
│   ├── weather_analyzer.py    # Weather data analysis
│   └── outfit_suggester.py    # Outfit suggestion generation
├── visualization/            # Visualization module
│   ├── __init__.py
│   └── chart_generator.py    # Chart generation with matplotlib
├── web_app.py                # Flask Web application
├── weather_agent.py          # CLI entry point
├── templates/                # HTML templates
│   └── index.html             # Web interface template
└── requirements.txt          # Python dependencies
```

### Module Description

| Module | Responsibility |
|--------|---------------|
| `config.py` | Centralized configuration management (API keys, URLs, timeouts) |
| `utils/` | Utility functions for Chinese text processing and weather code conversion |
| `api/` | Encapsulates weather API calls with a unified interface |
| `core/` | Core business logic for weather analysis and outfit suggestions |
| `visualization/` | Handles matplotlib chart generation |
| `web_app.py` | Flask web service, handles HTTP requests and conversation logic |
| `weather_agent.py` | CLI entry point, provides command-line interaction |

---

## 🔧 Tech Stack

| Category | Technology |
|----------|------------|
| **Language** | Python 3.8+ |
| **Web Framework** | Flask 2.0+ |
| **HTTP Client** | requests |
| **Data Visualization** | matplotlib |
| **Chinese Pinyin** | pypinyin |
| **Weather API** | [Open-Meteo](https://open-meteo.com/) (free), [HeFeng Weather](https://dev.heweather.com/) (paid) |

---

## 🚀 Quick Start

### Requirements

- Python 3.8 or higher
- pip package manager

### Installation

```bash
# Clone the project
git clone https://github.com/cang-ge/weather-agent.git
cd weather-agent

# Install dependencies
pip install -r requirements.txt
```

### Run

#### Web Interface (Recommended)

```bash
python web_app.py
<<<<<<< HEAD
```

Then open in browser: http://127.0.0.1:5000

#### Command Line Mode

```bash
# Query a single city
python weather_agent.py Beijing

# Interactive mode without arguments
python weather_agent.py
=======
>>>>>>> 17e338b607d6e9e589f2e84f22c59cbae6a12d49
```

---

## 📖 Usage Examples

### Web Interface

1. Enter a city name in the input box (e.g., "Beijing" or "北京")
2. Click send or press Enter
3. View weather info, outfit suggestions, and 7-day forecast charts

### Supported Query Formats

```
北京天气              → Query Beijing weather
上海怎么样             → Query Shanghai weather
帮我查询广州的天气      → Query Guangzhou weather
杭州穿什么合适          → Query Hangzhou weather and get outfit suggestions
Tokyo weather         → Query Tokyo weather (English)
伦敦天气怎么样          → Query London weather
```

### CLI Example

```
$ python weather_agent.py 北京

==================================================
  Querying weather for 北京...
==================================================

📍 Beijing Weather Details
   Data Source: Open-Meteo
   Current Weather: Cloudy
   Temperature: 11.5~24.7°C
   Precipitation: 0.0 mm

📅 7-Day Forecast:
   04-21: Cloudy 11.5~24.7°C  Precipitation:0.0mm
   ...

👗 Outfit Suggestions
==================================================
☀️ [WARM] Warm weather (20-25°C)
• T-shirt/Shirt + Light jacket (backup)
• Jeans/Long skirt
• Comfortable sneakers

==================================================
📊 Generating weather trend chart...
==================================================
✅ Chart saved: /path/to/beijing_weather_trend.png
```

---

## ⚙️ Configuration

### HeFeng Weather API (Optional)

HeFeng Weather requires registration to get an API key. To configure:

1. Register: https://dev.heweather.com/
2. Get your API Key
3. Set environment variable:
   ```bash
   export HEFENG_API_KEY="your_api_key_here"  # Linux/Mac
   set HEFENG_API_KEY=your_api_key_here        # Windows
   ```

**Note**: Without HeFeng API configuration, the program automatically uses Open-Meteo (free, no API key required)

---

## 🌐 API Sources

| API | Description | Cost |
|-----|-------------|------|
| [Open-Meteo](https://open-meteo.com/) | Primary weather data source, supports global cities | Free |
| [HeFeng Weather](https://dev.heweather.com/) | Optional advanced weather data source | Limited free tier |

---

## 📝 Design Principles

1. **Modularity**: Each feature is an independent module with clear responsibilities
2. **Extensibility**: Adding a new weather source only requires implementing the `WeatherProvider` interface
3. **Centralized Configuration**: All configuration is centrally managed for easy maintenance
4. **Error Handling**: Comprehensive exception catching and error reporting

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

---

## 📄 License

MIT License

---

## 🙏 Acknowledgments

- [Open-Meteo](https://open-meteo.com/) - Free weather API
- [PyPinyin](https://github.com/mozillazg/python-pypinyin) - Chinese pinyin conversion