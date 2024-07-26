import requests
from langchain.prompts import PromptTemplate
import re

API_KEY = "你的和风天气API密钥"

BOT_TAG_PATTERN = r"<bot>(.*?)</bot>"

# 定义提示模板...
# 此处省略了你之前定义的模板代码。

def get_api_url(location, api_key, endpoint):
    """
    根据给定参数构建API URL。
    """
    return f"https://{endpoint}?location={location}&key={api_key}"

def extract_bot_response(user_input):
    """
    从用户输入中提取被 <bot> 标签包裹的内容。
    """
    match = re.search(BOT_TAG_PATTERN, user_input)
    return match.group(1) if match else None

def fetch_weather_forecast(location, api_key):
    """
    获取天气预测的API调用。
    """
    url = get_api_url(location, api_key, 'devapi.qweather.com/s6/weather/forecast')
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()  # 或者 response.text 如果API返回的是纯文本
    except requests.RequestException as e:
        return f"Error fetching weather data: {e}"

# 示例使用
# 假设用户输入了以下内容
user_input = "待查询天气位置：天安门 <bot>https://geoapi.qweather.com/v2/city/lookup?location=天安门&key=你的API_KEY<bot>"

# 提取用户输入的API地址
api_url = extract_bot_response(user_input)
if api_url:
    # 假设我们已经有了LocationID和location_resp
    location_id = "从api_url解析得到的LocationID"
    location_resp = "从API调用得到的响应内容"
    
    # 构建并发送3日天气预报API请求
    weather_data = fetch_weather_forecast(location_id, API_KEY)
    print(weather_data)  # 打印或返回天气数据
