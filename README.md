# Weather Outfit Assistant / 智能天气穿搭助手

> Input a city name, get real-time weather forecasts and smart outfit recommendations.
> 输入城市名称，获取实时天气预报和智能穿搭建议

[English](#english) | [简体中文](#简体中文)

---

<a name="english"></a>

## Features

- **Multi-source Weather Data**: Supports Open-Meteo (free, no API key) and HeFeng Weather (paid API)
- **Smart Outfit Suggestions**: Professional clothing recommendations based on temperature and weather conditions
- **7-Day Forecast Charts**: Auto-generated temperature trend and precipitation visualization
- **Global City Support**: Supports Chinese and English city names with automatic conversion
- **Natural Language Queries**: Supports formats like "Beijing weather", "London weather怎么样"
- **Web Interface**: Feature-rich web client with quick city buttons

---

## Project Architecture

```
weather_agent/
├── config.py                 # Configuration (API keys, URLs, constants)
├── utils/                    # Utility modules
│   ├── __init__.py
│   ├── chinese_util.py       # Chinese text processing (pinyin, city mapping)
│   └── weather_codes.py      # WMO weather code mapping
├── api/                      # Weather API layer
│   ├── __init__.py
│   ├── weather_base.py       # Abstract base class for weather providers
│   ├── hefeng_api.py         # HeFeng Weather API implementation
│   └── openmeteo_api.py      # Open-Meteo API implementation
├── core/                     # Core business logic
│   ├── __init__.py
│   ├── weather_analyzer.py   # Weather data analysis
│   └── outfit_suggester.py   # Outfit suggestion generation
├── visualization/            # Visualization module
│   ├── __init__.py
│   └── chart_generator.py   # Chart generation with matplotlib
├── web_app.py               # Flask Web application
├── weather_agent.py         # CLI entry point
├── templates/               # HTML templates
│   └── index.html           # Web interface template
└── requirements.txt        # Python dependencies
```

---

## Tech Stack

| Category | Technology |
|----------|------------|
| **Language** | Python 3.8+ |
| **Web Framework** | Flask 2.0+ |
| **HTTP Client** | requests |
| **Data Visualization** | matplotlib |
| **Chinese Pinyin** | pypinyin |
| **Weather APIs** | [Open-Meteo](https://open-meteo.com/) (free), [HeFeng Weather](https://dev.heweather.com/) (paid) |

---

## Quick Start

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
```

Then open in browser: http://127.0.0.1:5000

#### Command Line Mode

```bash
# Query a single city
python weather_agent.py Beijing

# Interactive mode
python weather_agent.py
```

---

## Usage Examples

### Supported Query Formats

```
北京天气              → Query Beijing weather
上海怎么样             → Query Shanghai weather
帮我查询广州的天气      → Query Guangzhou weather
杭州穿什么合适          → Query Hangzhou weather with outfit suggestions
Tokyo weather         → Query Tokyo weather (English)
伦敦天气怎么样          → Query London weather (Chinese)
London weather        → Query London weather (English)
```

### Supported Cities

**Chinese Cities (by pinyin conversion):**
Beijing, Shanghai, Guangzhou, Shenzhen, Chengdu, Chongqing, Hangzhou, Wuhan, Xi'an, etc.

**Foreign Cities (by name mapping):**
London, Paris, Tokyo, New York, Sydney, Berlin, Rome, Moscow, Dubai, Singapore, etc.

---

## Configuration

### HeFeng Weather API (Optional)

HeFeng Weather requires registration. To configure:

1. Register at https://dev.heweather.com/
2. Get your API Key
3. Set environment variable:

```bash
# Linux/Mac
export HEFENG_API_KEY="your_api_key_here"

# Windows
set HEFENG_API_KEY=your_api_key_here
```

**Note**: Without HeFeng API, the program automatically uses Open-Meteo (free, no key required)

---

## API Sources

| API | Description | Cost |
|-----|-------------|------|
| [Open-Meteo](https://open-meteo.com/) | Primary data source, global city support | Free |
| [HeFeng Weather](https://dev.heweather.com/) | Optional advanced source | Limited free tier |

---

## Design Principles

1. **Modularity**: Each feature is an independent module with clear responsibilities
2. **Extensibility**: Adding a new weather source only requires implementing the `WeatherProvider` interface
3. **Centralized Configuration**: All configuration is centrally managed
4. **Error Handling**: Comprehensive exception catching and error reporting

---

## License

MIT License

---

## Acknowledgments

- [Open-Meteo](https://open-meteo.com/) - Free weather API
- [PyPinyin](https://github.com/mozillazg/python-pypinyin) - Chinese pinyin conversion

---

<a name="简体中文"></a>

## 功能特性

- **多源天气数据**: 支持 Open-Meteo（免费，无需API密钥）和和风天气（付费API）
- **智能穿搭建议**: 根据温度和天气状况生成专业穿搭推荐
- **7天预报图表**: 自动生成温度趋势和降水预报可视化图表
- **全球化城市支持**: 支持中文和英文城市名，自动转换
- **自然语言查询**: 支持多种格式，如"北京天气"、"伦敦天气怎么样"
- **Web界面**: 功能丰富的网页客户端，支持快捷城市按钮

---

## 项目架构

```
weather_agent/
├── config.py                 # 配置管理（API密钥、URL、常量）
├── utils/                    # 工具模块
│   ├── __init__.py
│   ├── chinese_util.py       # 中文处理（拼音转换、城市映射）
│   └── weather_codes.py      # WMO天气代码映射
├── api/                      # 天气API接口层
│   ├── __init__.py
│   ├── weather_base.py       # API基类（抽象接口）
│   ├── hefeng_api.py         # 和风天气API实现
│   └── openmeteo_api.py      # Open-Meteo API实现
├── core/                     # 核心业务逻辑
│   ├── __init__.py
│   ├── weather_analyzer.py   # 天气数据分析
│   └── outfit_suggester.py   # 穿搭建议生成
├── visualization/            # 可视化模块
│   ├── __init__.py
│   └── chart_generator.py   # 图表绘制（matplotlib）
├── web_app.py               # Flask Web应用
├── weather_agent.py         # CLI命令行入口
├── templates/               # HTML模板
│   └── index.html           # Web界面模板
└── requirements.txt        # Python依赖
```

---

## 技术栈

| 分类 | 技术 |
|------|------|
| **语言** | Python 3.8+ |
| **Web框架** | Flask 2.0+ |
| **HTTP客户端** | requests |
| **数据可视化** | matplotlib |
| **中文拼音** | pypinyin |
| **天气API** | [Open-Meteo](https://open-meteo.com/)（免费）、[和风天气](https://dev.heweather.com/)（付费） |

---

## 快速开始

### 环境要求

- Python 3.8 或更高版本
- pip 包管理器

### 安装

```bash
# 克隆项目
git clone https://github.com/cang-ge/weather-agent.git
cd weather-agent

# 安装依赖
pip install -r requirements.txt
```

### 运行

#### Web界面（推荐）

```bash
python web_app.py
```

然后在浏览器打开: http://127.0.0.1:5000

#### 命令行模式

```bash
# 查询单个城市
python weather_agent.py 北京

# 交互模式
python weather_agent.py
```

---

## 使用示例

### 支持的查询格式

```
北京天气              → 查询北京天气
上海怎么样             → 查询上海天气
帮我查询广州的天气      → 查询广州天气
杭州穿什么合适          → 查询杭州天气并获取穿搭建议
Tokyo weather         → 查询东京天气（英文）
伦敦天气怎么样          → 查询伦敦天气（中文）
London weather        → 查询伦敦天气（英文）
```

### 支持的城市

**中国城市（通过拼音转换）:**
北京、上海、广州、深圳、成都、重庆、杭州、武汉、西安等

**外国城市（通过名称映射）:**
伦敦、巴黎、东京、纽约、悉尼、柏林、罗马、莫斯科、迪拜、新加坡等

---

## 配置说明

### 和风天气API（可选）

和风天气需要注册获取API密钥。如需配置：

1. 注册账号: https://dev.heweather.com/
2. 获取API Key
3. 设置环境变量:

```bash
# Linux/Mac
export HEFENG_API_KEY="your_api_key_here"

# Windows
set HEFENG_API_KEY=your_api_key_here
```

**注意**: 不配置和风API时，程序将自动使用 Open-Meteo（免费无需API密钥）

---

## API来源

| API | 说明 | 费用 |
|-----|------|------|
| [Open-Meteo](https://open-meteo.com/) | 主要数据源，支持全球城市 | 免费 |
| [和风天气](https://dev.heweather.com/) | 可选的高级数据源 | 免费额度有限 |

---

## 设计原则

1. **模块化**: 每个功能独立成模块，职责清晰
2. **可扩展性**: 新增天气源只需实现 `WeatherProvider` 接口
3. **配置集中**: 所有配置集中管理，便于维护
4. **错误处理**: 完善的异常捕获和错误提示

---

## 许可证

MIT License

---

## 致谢

- [Open-Meteo](https://open-meteo.com/) - 免费天气API
- [PyPinyin](https://github.com/mozillazg/python-pypinyin) - 中文拼音转换