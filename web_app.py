"""
智能天气穿搭助手 - Web服务
功能：提供网页界面，支持对话交互
"""

from flask import Flask, render_template, request, jsonify
import os
import base64
import io
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

# 导入天气模块
from weather_agent import (
    get_weather_open_meteo,
    analyze_open_meteo_weather,
    get_outfit_suggestion,
    draw_weather_trend,
    get_weather_forecast,
    analyze_weather
)

app = Flask(__name__)
app.secret_key = os.urandom(24)

# 存储对话历史
conversations = {}

# ============== 页面路由 ==============

@app.route('/')
def index():
    """主页"""
    return render_template('index.html')

# ============== API路由 ==============

@app.route('/api/weather', methods=['POST'])
def api_weather():
    """查询天气"""
    data = request.get_json()
    city = data.get('city', '').strip()

    if not city:
        return jsonify({'error': '请输入城市名称'})

    weather_data = None
    source = "openmeteo"

    # 尝试和风天气
    from weather_agent import HEFENG_API_KEY
    if HEFENG_API_KEY and HEFENG_API_KEY != "YOUR_API_KEY_HERE":
        weather_data = get_weather_forecast(city, days=7)
        if weather_data:
            source = "hefeng"

    # 尝试Open-Meteo
    if not weather_data:
        weather_data = get_weather_open_meteo(city)
        if weather_data:
            source = "openmeteo"

    if not weather_data:
        return jsonify({'error': '无法获取天气数据，请检查城市名称或网络连接'})

    weather_info = analyze_weather(weather_data, source)
    outfit = get_outfit_suggestion(weather_info, source)

    # 生成图表
    chart_base64 = None
    if "未来几天" in weather_info:
        try:
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
            days = weather_info["未来几天"]
            dates = [d["日期"][-5:] for d in days]
            max_temps = [d["最高温"] for d in days]
            min_temps = [d["最低温"] for d in days]
            precipitation = [d["降水"] for d in days]

            ax1.plot(dates, max_temps, 'r-o', label='Max Temp', linewidth=2, markersize=8)
            ax1.plot(dates, min_temps, 'b-o', label='Min Temp', linewidth=2, markersize=8)
            ax1.fill_between(dates, min_temps, max_temps, alpha=0.3, color='orange')
            ax1.set_xlabel('Date')
            ax1.set_ylabel('Temperature (C)')
            ax1.set_title(f'{city} 7-Day Temperature Trend')
            ax1.legend(loc='upper right')
            ax1.grid(True, linestyle='--', alpha=0.7)

            ax2.bar(dates, precipitation, color='steelblue', alpha=0.8)
            ax2.set_xlabel('Date')
            ax2.set_ylabel('Precipitation (mm)')
            ax2.set_title(f'{city} 7-Day Precipitation Forecast')
            ax2.grid(True, linestyle='--', alpha=0.7, axis='y')

            plt.tight_layout()

            buf = io.BytesIO()
            plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
            buf.seek(0)
            chart_base64 = base64.b64encode(buf.read()).decode('utf-8')
            plt.close()
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
    """对话交互"""
    data = request.get_json()
    message = data.get('message', '').strip()
    session_id = data.get('session_id', 'default')

    # 初始化会话
    if session_id not in conversations:
        conversations[session_id] = []

    # 常见城市列表（按长度降序排列，避免"北京"匹配了"北京天气"中的"北京天气"）
    common_cities = [
        '北京', '上海', '广州', '深圳', '杭州', '南京', '成都', '重庆',
        '武汉', '西安', '苏州', '天津', '长沙', '郑州', '青岛', '济南',
        '南昌', '大连', '沈阳', '哈尔滨', '长春', '福州', '厦门', '泉州', '南宁',
        '桂林', '昆明', '贵阳', '太原', '石家庄', '兰州', '西宁', '银川',
        '乌鲁木齐', '拉萨', '呼和浩特', '海口', '三亚', '珠海', '佛山', '东莞',
        '无锡', '常州', '徐州', '南通', '扬州', '镇江', '盐城', '泰州',
        'beijing', 'shanghai', 'guangzhou', 'shenzhen', 'hangzhou',
        'nanjing', 'chengdu', 'chongqing', 'wuhan', 'xian', 'suzhou', 'nanchang',
        'tokyo', 'osaka', 'seoul', 'bangkok', 'singapore', 'new york', 'london', 'paris'
    ]

    # 解析城市名 - 优先精确匹配
    city = None
    message_lower = message.lower()

    # 1. 尝试直接匹配城市名
    for c in common_cities:
        if c.lower() == message_lower or c.lower() == message_lower.replace(' ', ''):
            city = c
            break

    # 2. 尝试从"XX天气/怎么样/如何"等模式中提取城市
    if not city:
        # 去掉常见后缀词来提取城市
        suffixes = ['天气', 'weather', '怎么样', '如何', '好吗', '查询', '看看', '帮我查', '请问']
        temp_msg = message
        for suffix in suffixes:
            temp_msg = temp_msg.replace(suffix, '').strip()
        # 检查清理后的内容是否是城市名
        for c in common_cities:
            if c.lower() == temp_msg.lower():
                city = c
                break

    # 3. 检查原始消息是否包含城市名
    if not city:
        for c in common_cities:
            if c.lower() in message_lower:
                city = c
                break

    if city:
        weather_data = get_weather_open_meteo(city)
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

    help_text = """你好！我是天气穿搭助手 🌤️

你可以这样问我：
• "北京天气"
• "上海天气怎么样"
• "帮我查询广州的天气"
• "杭州穿什么合适"

或者直接输入城市名也可以哦！"""

    return jsonify({'response': help_text, 'type': 'help'})

# ============== 启动 ==============

if __name__ == '__main__':
    print("=" * 50)
    print("Weather Outfit Assistant Web Server")
    print("=" * 50)
    print("Open: http://127.0.0.1:5000")
    print("=" * 50)
    app.run(host='0.0.0.0', port=5000, debug=True)
