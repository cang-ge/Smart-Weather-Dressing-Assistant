"""
智能天气穿搭助手
功能：输入城市 -> 获取天气数据 -> 分析天气 -> 绘制趋势图 -> 给出穿搭建议
"""

import requests
import json
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Tuple
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# ============== 配置 ==============
# 和风天气API (需要注册获取KEY: https://dev.heweather.com/)
HEFENG_API_KEY = "de270305f9784be3be947b56f5af7d48"
# 开发版统一使用 devapi 域名
HEFENG_BASE_URL = "https://devapi.heweather.com/v7"

# Open-Meteo (免费无需API)
OPEN_METEO_BASE_URL = "https://api.open-meteo.com/v1/forecast"

# ============== 天气数据获取 ==============

def get_weather_forecast(city_name: str, days: int = 7) -> Optional[Dict]:
    """获取天气预报 (和风天气) - 直接使用城市中文名请求"""
    session = requests.Session()
    session.trust_env = True # 自动使用系统代理
    
    # 优化：v7 接口支持直接传中文名，无需先查 ID，减少一次网络请求
    url = f"{HEFENG_BASE_URL}/weather/{days}d?location={city_name}&key={HEFENG_API_KEY}"
    
    print(f"  -> 请求URL: {url}") # 调试用，可看请求是否发出
    
    try:
        resp = session.get(url, timeout=15)
        print(f"  -> HTTP状态码: {resp.status_code}")
        
        data = resp.json()
        code = data.get("code")
        
        # 详细业务逻辑报错
        if code == "200":
            return data
        elif code == "401":
            print("  -> [错误] Key 无效或已过期")
        elif code == "403":
            print("  -> [错误] 权限不足！请检查控制台是否勾选了对应的 API 接口权限。")
        elif code == "404":
            print("  -> [错误] 找不到该城市，请尝试输入城市拼音或 ID。")
        else:
            print(f"  -> [错误] API 返回: {code} - {data.get('msg', '未知错误')}")
            
    except requests.exceptions.ConnectionError as e:
        print(f"  -> [网络错误] 无法连接到和风服务器，请检查 DNS 或开启代理。详情: {e}")
    except Exception as e:
        print(f"  -> [异常] {e}")
        
    return None

def get_weather_open_meteo(city_name: str) -> Optional[Dict]:
    """使用Open-Meteo API获取天气 (免费无需API)"""
    # 尝试不同的地理编码接口
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=zh"
    try:
        print(f"  -> 正在解析城市坐标: {city_name}...")
        geo_resp = requests.get(geo_url, timeout=15)
        geo_resp.raise_for_status() # 检查 HTTP 错误
        geo_data = geo_resp.json()
        
        if not geo_data.get("results"):
            print(f"  -> 未找到城市: {city_name}")
            return None

        lat = geo_data["results"][0]["latitude"]
        lon = geo_data["results"][0]["longitude"]
        timezone = geo_data["results"][0].get("timezone", "Asia/Shanghai")
        print(f"  -> 坐标获取成功: {lat}, {lon}")

        weather_url = f"{OPEN_METEO_BASE_URL}?latitude={lat}&longitude={lon}&timezone={timezone}&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,weathercode&forecast_days=7"
        
        print(f"  -> 正在获取天气数据...")
        weather_resp = requests.get(weather_url, timeout=15)
        weather_resp.raise_for_status()
        return weather_resp.json()
    except requests.exceptions.ConnectionError as e:
        print(f"  -> [网络连接错误] 无法连接到 Open-Meteo: {e}")
        print("     提示: 请检查是否需要开启系统代理或 VPN。")
    except requests.exceptions.Timeout:
        print(f"  -> [超时] 请求 Open-Meteo 超时，请检查网络速度。")
    except Exception as e:
        print(f"  -> Open-Meteo查询失败: {e}")
    return None

# ============== 天气分析 ==============

def analyze_weather(weather_data: Dict, source: str = "hefeng") -> Dict:
    """分析天气数据"""
    if source == "hefeng":
        return analyze_hefeng_weather(weather_data)
    else:
        return analyze_open_meteo_weather(weather_data)

def analyze_hefeng_weather(data: Dict) -> Dict:
    """解析和风天气数据"""
    result = {"source": "和风天气"}
    try:
        now = data.get("now", {})
        result["温度"] = f"{now.get('temp', 'N/A')}C"
        result["体感温度"] = f"{now.get('feelsLike', 'N/A')}C"
        result["天气状况"] = now.get('text', '未知')
        result["风速"] = f"{now.get('windSpeed', 'N/A')} km/h"
        result["风速等级"] = now.get('windScale', '未知')
        result["湿度"] = f"{now.get('humidity', 'N/A')}%"
        result["气压"] = f"{now.get('pressure', 'N/A')} hPa"
    except Exception as e:
        print(f"解析失败: {e}")
    return result

def analyze_open_meteo_weather(data: Dict) -> Dict:
    """解析Open-Meteo天气数据"""
    result = {"source": "Open-Meteo"}
    try:
        daily = data.get("daily", {})
        times = daily.get("time", [])
        if times:
            result["日期"] = times[0]
            result["最高温度"] = f"{daily['temperature_2m_max'][0]}C"
            result["最低温度"] = f"{daily['temperature_2m_min'][0]}C"
            result["温度"] = f"{daily['temperature_2m_min'][0]}~{daily['temperature_2m_max'][0]}C"
            result["降水"] = f"{daily['precipitation_sum'][0]} mm"
            result["天气代码"] = daily['weathercode'][0]
            result["天气状况"] = weather_code_to_text(daily['weathercode'][0])
            result["未来几天"] = []

            for i in range(min(7, len(times))):
                result["未来几天"].append({
                    "日期": times[i],
                    "最高温": daily['temperature_2m_max'][i],
                    "最低温": daily['temperature_2m_min'][i],
                    "天气": weather_code_to_text(daily['weathercode'][i]),
                    "降水": daily['precipitation_sum'][i]
                })
    except Exception as e:
        print(f"解析失败: {e}")
    return result

def weather_code_to_text(code: int) -> str:
    """WMO天气代码转中文"""
    codes = {
        0: "晴", 1: "晴间多云", 2: "多云", 3: "阴",
        45: "雾", 48: "霜雾",
        51: "小毛毛雨", 53: "中毛毛雨", 55: "大毛毛雨",
        61: "小雨", 63: "中雨", 65: "大雨",
        71: "小雪", 73: "中雪", 75: "大雪",
        80: "小阵雨", 81: "中阵雨", 82: "大阵雨",
        95: "雷暴", 96: "雷暴+冰雹", 99: "雷暴+大雨"
    }
    return codes.get(code, f"未知({code})")

# ============== 穿搭建议 ==============

def get_outfit_suggestion(weather_info: Dict, source: str = "hefeng") -> str:
    """根据天气生成穿搭建议"""
    if source == "hefeng":
        return get_outfit_hefeng(weather_info)
    else:
        return get_outfit_open_meteo(weather_info)

def get_outfit_hefeng(weather: Dict) -> str:
    """和风天气穿搭建议"""
    temp_str = weather.get("温度", "0C").replace("C", "")
    try:
        temp = int(temp_str)
    except:
        temp = 20

    condition = weather.get("天气状况", "")
    feels_like_str = weather.get("体感温度", "0C").replace("C", "")
    try:
        feels_like = int(feels_like_str)
    except:
        feels_like = temp

    return generate_outfit_text(temp, feels_like, condition)

def get_outfit_open_meteo(weather: Dict) -> str:
    """Open-Meteo穿搭建议"""
    temp_str = weather.get("温度", "20C").replace("C", "")
    try:
        if "~" in temp_str:
            parts = temp_str.split("~")
            temp = (int(parts[0]) + int(parts[1].replace("C", ""))) // 2
        else:
            temp = int(temp_str.replace("C", ""))
    except:
        temp = 20

    condition = weather.get("天气状况", "")
    return generate_outfit_text(temp, temp, condition)

def generate_outfit_text(temp: int, feels_like: int, condition: str) -> str:
    """生成穿搭建议文本"""
    suggestions = []

    if temp < 0:
        suggestions.append("[FREEZING] 严寒天气（<0C）")
        suggestions.append("- 羽绒服/厚棉服 + 保暖内衣")
        suggestions.append("- 围巾 + 手套 + 帽子")
        suggestions.append("- 雪地靴或厚棉鞋")
    elif temp < 10:
        suggestions.append("[COLD] 寒冷天气（0-10C）")
        suggestions.append("- 棉衣/轻薄羽绒服 + 毛衣/卫衣")
        suggestions.append("- 牛仔裤/保暖裤")
        suggestions.append("- 围巾（防风）")
    elif temp < 15:
        suggestions.append("[COOL] 凉意天气（10-15C）")
        suggestions.append("- 薄外套/夹克 + 衬衫/T恤")
        suggestions.append("- 长裤/休闲裤")
        suggestions.append("- 早晚建议加件薄针织衫")
    elif temp < 20:
        suggestions.append("[COMFORTABLE] 舒适天气（15-20C）")
        suggestions.append("- 薄长袖 + 休闲外套")
        suggestions.append("- 牛仔裤/休闲裤")
        suggestions.append("- 单鞋或运动鞋")
    elif temp < 25:
        suggestions.append("[WARM] 温暖天气（20-25C）")
        suggestions.append("- T恤/衬衫 + 薄外套（备用）")
        suggestions.append("- 牛仔裤/长裙")
        suggestions.append("- 舒适运动鞋")
    elif temp < 30:
        suggestions.append("[HOT] 炎热天气（25-30C）")
        suggestions.append("- 短袖 + 轻薄长裤")
        suggestions.append("- 遮阳帽/太阳镜")
        suggestions.append("- 透气运动鞋")
    else:
        suggestions.append("[VERY HOT] 高温天气（>30C）")
        suggestions.append("- 透气短袖/背心")
        suggestions.append("- 短裤/轻薄长裤")
        suggestions.append("- 防晒 + 充足补水")

    if "雨" in condition or "雪" in condition:
        suggestions.append("\n[RAIN] 雨雪天气提示:")
        suggestions.append("- 请携带雨伞/雨衣")
        suggestions.append("- 穿防滑鞋，避免滑倒")
        if temp < 15:
            suggestions.append("- 建议穿防水外套")

    if "雾" in condition or "霾" in condition:
        suggestions.append("\n[FOG] 雾霾天气提示:")
        suggestions.append("- 佩戴口罩")
        suggestions.append("- 穿亮色系衣服便于识别")
        suggestions.append("- 驾车请注意安全")

    if "晴" in condition and temp > 25:
        suggestions.append("\n[SUNNY] 晴天防晒提示:")
        suggestions.append("- 涂抹防晒霜")
        suggestions.append("- 戴遮阳帽或撑伞")

    return "\n".join(suggestions)

# ============== 图表绘制 ==============

def draw_weather_trend(weather_info: Dict, city_name: str, save_path: str = None):
    """绘制天气趋势图"""
    if "未来几天" not in weather_info:
        print("没有足够数据绘制趋势图")
        return

    days = weather_info["未来几天"]
    dates = [d["日期"][-5:] for d in days]
    max_temps = [d["最高温"] for d in days]
    min_temps = [d["最低温"] for d in days]
    precipitation = [d["降水"] for d in days]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

    ax1.plot(dates, max_temps, 'r-o', label='Max Temp', linewidth=2, markersize=8)
    ax1.plot(dates, min_temps, 'b-o', label='Min Temp', linewidth=2, markersize=8)
    ax1.fill_between(dates, min_temps, max_temps, alpha=0.3, color='orange')
    ax1.set_xlabel('Date', fontsize=12)
    ax1.set_ylabel('Temperature (C)', fontsize=12)
    ax1.set_title(f'{city_name} 7-Day Temperature Trend', fontsize=14, fontweight='bold')
    ax1.legend(loc='upper right')
    ax1.grid(True, linestyle='--', alpha=0.7)

    ax2.bar(dates, precipitation, color='steelblue', alpha=0.8)
    ax2.set_xlabel('Date', fontsize=12)
    ax2.set_ylabel('Precipitation (mm)', fontsize=12)
    ax2.set_title(f'{city_name} 7-Day Precipitation Forecast', fontsize=14, fontweight='bold')
    ax2.grid(True, linestyle='--', alpha=0.7, axis='y')

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"图表已保存: {save_path}")
    else:
        plt.savefig(f"{city_name}_weather_trend.png", dpi=150, bbox_inches='tight')
        print(f"图表已保存: {city_name}_weather_trend.png")

    plt.close()

# ============== 主程序 ==============

def main():
    print("=" * 50)
    print("* Weather Outfit Assistant *")
    print("=" * 50)

    city = input("\n请输入城市名称（如：北京、上海、广州）: ").strip()
    if not city:
        print("城市名称不能为空")
        return

    print(f"\n正在查询 {city} 的天气信息...\n")

    weather_data = None
    source = "openmeteo" 

    # 优先尝试和风天气
    if HEFENG_API_KEY and HEFENG_API_KEY != "YOUR_API_KEY_HERE":
        print("[1/2] 正在尝试连接和风天气...")
        weather_data = get_weather_forecast(city, days=7)
        if weather_data:
            source = "hefeng"
        else:
            print("    [WARN] 和风天气获取失败，准备切换至备用线路...\n")
    
    # 如果和风失败或未配置，使用 Open-Meteo
    if not weather_data:
        print("[2/2] 正在使用 Open-Meteo 天气API (免费免登录)...")
        weather_data = get_weather_open_meteo(city)
        if weather_data:
            source = "openmeteo"

    if not weather_data:
        print("\n" + "=" * 50)
        print("[ERROR] 最终结果: 无法获取天气数据")
        print("建议排查:")
        print("1. 检查电脑是否可以正常访问网页 (如 baidu.com)")
        print("2. 如果使用了代理软件，请确认已开启‘系统代理’或‘TUN模式’")
        print("3. 尝试更换网络环境 (如手机热点)")
        print("=" * 50)
        return

    weather_info = analyze_weather(weather_data, source)

    print("=" * 50)
    print(f"## {city} 天气详情")
    print("=" * 50)

    if source == "hefeng":
        for key, value in weather_info.items():
            if key != "source":
                print(f"  {key}: {value}")
    else:
        print(f"  数据来源: {weather_info.get('source', '未知')}")
        print(f"  当前天气: {weather_info.get('天气状况', '未知')}")
        print(f"  温度: {weather_info.get('温度', '未知')}")
        print(f"  降水: {weather_info.get('降水', '未知')}")

        if "未来几天" in weather_info:
            print("\n>> 未来一周预报:")
            for day in weather_info["未来几天"]:
                date_str = day["日期"][-5:]
                print(f"  {date_str}: {day['天气']} {day['最低温']}~{day['最高温']}C 降水:{day['降水']}mm")

    print("\n" + "=" * 50)
    print(">> 穿搭建议")
    print("=" * 50)
    outfit = get_outfit_suggestion(weather_info, source)
    print(outfit)

    if "未来几天" in weather_info:
        print("\n" + "=" * 50)
        print(">> 正在生成天气趋势图...")
        print("=" * 50)
        save_path = os.path.join(os.getcwd(), f"{city}_weather_trend.png")
        draw_weather_trend(weather_info, city, save_path)

    print("\n[DONE] 查询完成！")

if __name__ == "__main__":
    main()
