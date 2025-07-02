import aiohttp
from typing import Dict, Any, Optional

from ..config import settings
from .base import BaseTool

class WeatherTool(BaseTool):
    """
    Tool for retrieving weather information for a specified location.
    """
    
    def __init__(self):
        super().__init__(
            name="weather",
            description="Get current weather information for a location"
        )
        self.api_key = settings.TOOL_CONFIGS["weather"]["api_key"]
        self.default_location = settings.TOOL_CONFIGS["weather"]["default_location"]
    
    @property
    def parameters(self) -> Dict[str, Any]:
        """Define the parameters for the weather tool."""
        return {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City name or location to get weather for"
                },
                "units": {
                    "type": "string",
                    "enum": ["metric", "imperial"],
                    "description": "Units for temperature (metric=Celsius, imperial=Fahrenheit)"
                }
            },
            "required": ["location"]
        }
    
    async def execute(self, location: str = None, units: str = "metric") -> Dict[str, Any]:
        """
        Get weather for the specified location.
        
        Args:
            location: City or location name
            units: 'metric' or 'imperial'
            
        Returns:
            Dict with weather information
        """
        location = location or self.default_location
        
        # Use OpenWeatherMap API (you would need an API key)
        url = f"https://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": location,
            "units": units,
            "appid": self.api_key
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"Weather API error: {error_text}")
                
                data = await response.json()
                
                # Format the response
                return {
                    "location": f"{data['name']}, {data.get('sys', {}).get('country', '')}",
                    "temperature": {
                        "current": data["main"]["temp"],
                        "feels_like": data["main"]["feels_like"],
                        "min": data["main"]["temp_min"],
                        "max": data["main"]["temp_max"],
                        "unit": "°C" if units == "metric" else "°F"
                    },
                    "humidity": data["main"]["humidity"],
                    "wind": {
                        "speed": data["wind"]["speed"],
                        "unit": "m/s" if units == "metric" else "mph"
                    },
                    "conditions": data["weather"][0]["main"],
                    "description": data["weather"][0]["description"],
                    "timestamp": data["dt"]
                }
    
    def format_for_llm(self, result: Dict[str, Any]) -> str:
        """Format the weather data for the LLM in a more readable way."""
        if result.get("status") == "error":
            return f"Error getting weather: {result.get('error')}"
        
        data = result.get("result", {})
        temp = data.get("temperature", {})
        unit = temp.get("unit", "°C")
        
        return (
            f"Weather in {data.get('location')}:\n"
            f"- Conditions: {data.get('description')}\n"
            f"- Temperature: {temp.get('current')}{unit} (feels like {temp.get('feels_like')}{unit})\n"
            f"- Humidity: {data.get('humidity')}%\n"
            f"- Wind: {data.get('wind', {}).get('speed')} {data.get('wind', {}).get('unit')}"
        )
