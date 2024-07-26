from pkg.plugin.context import register, llm_func, BasePlugin, APIHost
import requests

@register(name="Weather", description="Provides weather information", version="0.1", author="daskm")
class WeatherPlugin(BasePlugin):

    def __init__(self, host: APIHost):
        # 初始化方法，插件加载时触发
        self.host = host

    async def initialize(self):
        # 异步初始化方法，插件加载时触发
        pass

    @llm_func(name="get_weather")
    async def get_weather(self, city: str) -> str:
        """
        Query the weather for a specified city.

        Args:
            city (str): The city to query the weather for.

        Returns:
            str: The weather information for the city.
        """
        API_KEY = 'your_api_key_here'  # Replace with your actual API key
        API_URL = 'http://api.openweathermap.org/data/2.5/weather'

        params = {
            'q': city,
            'appid': API_KEY,
            'units': 'metric'
        }

        response = requests.get(API_URL, params=params)
        weather_data = response.json()

        if weather_data['cod'] != 200:
            return f"Error: {weather_data['message']}"

        main = weather_data['weather'][0]['main']
        description = weather_data['weather'][0]['description']
        temperature = weather_data['main']['temp']

        return f"The weather in {city} is currently {main} with a temperature of {temperature}°C and a description of {description}."

    def __del__(self):
        # 插件卸载时触发
        pass
