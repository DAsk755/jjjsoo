import re
import datetime
import requests
import logging

from pkg.plugin.models import *
from pkg.plugin.host import EventContext, PluginHost

# 导入模板和API_KEY
from plugins.WeatherPlugin.template import API_KEY, BOT_TAG_PATTERN, LOCATION_PROMPT, API_PROMPT, WEATHER_PROMPT

# 设置日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# 注册插件
@register(name="Weather", description="和风天气查询", version="0.1", author="lieyanqzu")
class WeatherPlugin(Plugin):

    def __init__(self, plugin_host: PluginHost):
        self.plugin_host = plugin_host
        # 其他初始化代码...

    async def send_api_request(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()  # 或者 response.text，取决于API返回的格式
        except requests.RequestException as e:
            logger.error(f"API请求失败: {e}")
            return None

    # 其他插件方法...

    def normal_message_received(self, event: EventContext, **kwargs):
        msg = kwargs['text_message']
        if "天气 " in msg:
            location = msg[len("天气 "):]
            # 构建和发送API请求
            location_url = self.build_api_url(location, "city/lookup")
            location_resp = self.send_api_request(location_url)
            
            if location_resp:
                weather_url = self.build_api_url(location_resp['location'], "weather/3d")
                weather_resp = self.send_api_request(weather_url)
                
                if weather_resp:
                    # 处理和转换API响应为自然语言
                    weather_info = self.format_weather_info(weather_resp, datetime.date.today())
                    event.add_return("reply", [weather_info])
            
            event.prevent_default()
            event.prevent_postorder()

    def build_api_url(self, location, endpoint):
        base_url = "https://devapi.qweather.com/v7"
        return f"{base_url}/{endpoint}?location={location}&key={API_KEY}"

    def format_weather_info(self, api_resp, today_date):
        # 根据API响应格式化天气信息
        # 这里需要根据实际API响应的结构来实现格式化逻辑
        pass

# 插件卸载和其他方法...
