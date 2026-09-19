"""Weather API wrapper for Sense-7."""

import requests
from typing import Dict, Optional


class WeatherAPI:
    """Fetch weather data from Open-Meteo (free, no API key needed)."""
    
    BASE_URL = "https://api.open-meteo.com/v1/forecast"
    
    def __init__(self):
        self.session = requests.Session()
    
    def get_forecast(self, lat: float, lon: float, days: int = 3) -> Optional[Dict]:
        """Get weather forecast for coordinates."""
        params = {
            "latitude": lat,
            "longitude": lon,
            "hourly": (
                "temperature_2m,relativehumidity_2m,"
                "precipitation_probability,surface_pressure,"
                "cloudcover,windspeed_10m"
            ),
            "forecast_days": days,
            "timezone": "auto"
        }
        
        try:
            response = self.session.get(self.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"API Error: {e}")
            return None
    
    def get_current_conditions(self, lat: float, lon: float) -> Dict:
        """Extract current conditions from forecast."""
        data = self.get_forecast(lat, lon, days=1)
        if not data:
            return {}
        
        # Get first hour's data (current-ish)
        hourly = data.get("hourly", {})
        return {
            "temperature": hourly["temperature_2m"][0],
            "humidity": hourly["relativehumidity_2m"][0],
            "pressure": hourly["surface_pressure"][0],
            "cloud_cover": hourly["cloudcover"][0],
            "wind_speed": hourly["windspeed_10m"][0],
            "rain_prob": hourly["precipitation_probability"][0] or 0
        }
