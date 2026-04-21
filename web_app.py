"""
智能天气穿搭助手 - Web服务
===========================
Flask Web界面，支持对话交互和天气查询

Features:
    - 自然语言城市天气查询
    - 智能穿搭建议
    - 7天天气预报图表
    - 多城市快捷查询

Run:
    python web_app.py
    Open: http://127.0.0.1:5000
"""

import os
import sys
import base64
import io

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template, request, jsonify
import matplotlib.pyplot as plt

# Suppress SSL warnings
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Import from modular structure
from core import get_weather_info, get_outfit_suggestion, analyze_open_meteo_weather
from api import get_open_meteo_weather
from visualization import draw_weather_trend
from config import configure_matplotlib

# Configure matplotlib for Chinese fonts
configure_matplotlib()

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Store conversation history
conversations = {}

# ============== 页面路由 ==============

@app.route('/')
def index():
    """主页"""
    return render_template('index.html')

# ============== API路由 ==============

@app.route('/api/weather', methods=['POST'])
def api_weather():
    """查询天气 - 返回完整天气信息和图表"""
    data = request.get_json()
    city = data.get('city', '').strip()

    if not city:
        return jsonify({'error': '请输入城市名称'})

    # Get weather info
    weather_info, source = get_weather_info(city)

    if not weather_info:
        return jsonify({'error': '无法获取天气数据，请检查城市名称或网络连接'})

    # Get outfit suggestion
    outfit = get_outfit_suggestion(weather_info, source)

    # Generate chart
    chart_base64 = None
    if "未来几天" in weather_info:
        try:
            fig = draw_weather_trend(weather_info, city)
            if fig:
                buf = io.BytesIO()
                plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
                buf.seek(0)
                chart_base64 = base64.b64encode(buf.read()).decode('utf-8')
                plt.close(fig)
        except Exception as e:
            print(f"图表生成失败: {e}")

    return jsonify({
        'city': city,
        'source': weather_info.get('source', '未知'),
        'weather': weather_info.get('天气状况', '未知'),
        'temp': weather_info.get('温度', '未知'),
        'forecast': weather_info.get('未来几天', []),
        'outfit': outfit,
        'chart': chart_base64
    })


@app.route('/api/chat', methods=['POST'])
def api_chat():
    """对话交互 - 解析城市名并返回天气信息"""
    data = request.get_json()
    message = data.get('message', '').strip()
    session_id = data.get('session_id', 'default')

    # Initialize conversation
    if session_id not in conversations:
        conversations[session_id] = []

    # Parse city name from message
    city = extract_city_from_message(message)

    if city:
        # Get weather directly from Open-Meteo for chat responses
        weather_data = get_open_meteo_weather(city)
        if weather_data:
            weather_info = analyze_open_meteo_weather(weather_data)
            outfit = get_outfit_suggestion(weather_info, 'openmeteo')

            response = f"📍 {city} 天气\n"
            response += f"天气: {weather_info.get('天气状况', '未知')}\n"
            response += f"温度: {weather_info.get('温度', '未知')}\n\n"
            response += f"👗 穿搭建议:\n{outfit}"

            conversations[session_id].append({'role': 'assistant', 'content': response})
            return jsonify({'response': response, 'type': 'weather'})
        else:
            response = f"抱歉，无法获取 {city} 的天气数据，请检查城市名称是否正确。"
            return jsonify({'response': response, 'type': 'error'})

    # Show help text for unrecognized input
    help_text = """你好！我是天气穿搭助手 🌤️

你可以这样问我：
• "北京天气"
• "上海天气怎么样"
• "帮我查询广州的天气"
• "杭州穿什么合适"
• "Tokyo weather"

或者直接输入城市名也可以哦！"""

    return jsonify({'response': help_text, 'type': 'help'})


def extract_city_from_message(message: str) -> str:
    """
    Extract city name from user message.

    Supports:
    - Direct city name: "北京", "Shanghai"
    - Weather queries: "北京天气", "上海 weather"
    - Outfit queries: "杭州穿什么"
    - Mixed patterns: "帮我查询广州的天气"

    Args:
        message: User input message

    Returns:
        Extracted city name or None
    """
    from utils import is_chinese

    # Common cities list (prioritized by length to avoid partial matches)
    common_cities = [
        '北京', '上海', '广州', '深圳', '杭州', '南京', '成都', '重庆',
        '武汉', '西安', '苏州', '天津', '长沙', '郑州', '青岛', '济南',
        '南昌', '大连', '沈阳', '哈尔滨', '长春', '福州', '厦门', '泉州',
        '南宁', '桂林', '昆明', '贵阳', '太原', '石家庄', '兰州', '西宁',
        '银川', '乌鲁木齐', '拉萨', '呼和浩特', '海口', '三亚', '珠海',
        '佛山', '东莞', '无锡', '常州', '徐州', '南通', '扬州', '镇江',
        '盐城', '泰州',
        'beijing', 'shanghai', 'guangzhou', 'shenzhen', 'hangzhou',
        'nanjing', 'chengdu', 'chongqing', 'wuhan', 'xian', 'suzhou',
        'tokyo', 'osaka', 'seoul', 'bangkok', 'singapore',
        'new york', 'london', 'paris', 'berlin', 'sydney', 'toronto'
    ]

    message_lower = message.lower().strip()

    # 1. Try exact match (city name only)
    for c in common_cities:
        if c.lower() == message_lower or c.lower() == message_lower.replace(' ', ''):
            return c

    # 2. Try to extract from patterns like "XX天气", "XX weather"
    suffixes = ['天气', 'weather', '怎么样', '如何', '好吗', '查询', '看看',
                '帮我查', '请问', '穿什么', '穿搭', '带什么']
    temp_msg = message
    for suffix in suffixes:
        temp_msg = temp_msg.replace(suffix, '').strip()

    for c in common_cities:
        if c.lower() == temp_msg.lower():
            return c

    # 3. Check if any city name is contained in the message
    for c in common_cities:
        if c.lower() in message_lower:
            return c

    return None


# ============== 启动 ==============

if __name__ == '__main__':
    print("=" * 50)
    print("  🌤️  Weather Outfit Assistant Web Server  🌤️")
    print("=" * 50)
    print("  📍 Open: http://127.0.0.1:5000")
    print("=" * 50)
    app.run(host='0.0.0.0', port=5000, debug=True)