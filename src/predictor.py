"""
Rain prediction logic for Sense-7.
Uses weighted factors: humidity, pressure, cloud cover, wind.
"""

from typing import Dict


class RainPredictor:
    """Predict rain probability based on weather factors."""
    
    # Weights for different factors (must sum to 1.0)
    WEIGHTS = {
        "humidity": 0.35,      # Most important
        "cloud_cover": 0.25,
        "pressure": 0.20,
        "api_rain_prob": 0.15,
        "wind": 0.05
    }
    
    def __init__(self):
        self.factors = {}
    
    def predict_rain(self, api_data: Dict) -> Dict:
        """
        Calculate rain probability from API data.
        Returns dict with probability, factors, and advice.
        """
        if not api_data or "hourly" not in api_data:
            return self._default_result()
        
        hourly = api_data["hourly"]
        
        # Get averages for next 12 hours (better prediction)
        hours = 12
        temp = sum(hourly["temperature_2m"][:hours]) / hours
        humidity = sum(hourly["relativehumidity_2m"][:hours]) / hours
        cloud = sum(hourly["cloudcover"][:hours]) / hours
        pressure = sum(hourly["surface_pressure"][:hours]) / hours
        wind = sum(hourly["windspeed_10m"][:hours]) / hours
        
        api_rain = hourly.get("precipitation_probability", [0] * hours)
        api_rain_avg = sum(x or 0 for x in api_rain[:hours]) / hours
        
        # ─────────────────────────────────────────────────────
        # CALCULATE SCORES (0-100 each)
        # ─────────────────────────────────────────────────────
        
        # Humidity score (>70% = high rain chance)
        humidity_score = min(100, (humidity / 80) * 100)
        
        # Cloud cover score
        cloud_score = min(100, (cloud / 90) * 100)
        
        # Pressure score (low pressure = rain)
        # Normal: 1013 hPa. <1000 = storm likely
        pressure_score = max(0, min(100, ((1020 - pressure) / 30) * 100))
        
        # API's own prediction (if available)
        api_score = api_rain_avg
        
        # Wind score (high wind + other factors = storm)
        wind_score = min(100, (wind / 30) * 100)
        
        # ─────────────────────────────────────────────────────
        # WEIGHTED AVERAGE
        # ─────────────────────────────────────────────────────
        rain_prob = (
            humidity_score * self.WEIGHTS["humidity"] +
            cloud_score * self.WEIGHTS["cloud_cover"] +
            pressure_score * self.WEIGHTS["pressure"] +
            api_score * self.WEIGHTS["api_rain_prob"] +
            wind_score * self.WEIGHTS["wind"]
        )
        
        rain_prob = max(0, min(100, round(rain_prob, 1)))
        
        # ─────────────────────────────────────────────────────
        # GENERATE ADVICE
        # ─────────────────────────────────────────────────────
        tip = self._generate_tip(rain_prob, humidity, pressure)
        
        return {
            "rain_probability": rain_prob,
            "temperature": round(temp, 1),
            "humidity": round(humidity, 1),
            "cloud_cover": round(cloud, 1),
            "pressure": round(pressure, 1),
            "wind_speed": round(wind, 1),
            "factors": {
                "humidity_score": round(humidity_score, 1),
                "cloud_score": round(cloud_score, 1),
                "pressure_score": round(pressure_score, 1)
            },
            "tip": tip
        }
    
    def _generate_tip(self, rain_prob: float, humidity: float, pressure: float) -> str:
        """Generate contextual advice."""
        if rain_prob >= 80:
            return "⚠️ Take umbrella! Heavy rain expected. Avoid low-lying areas."
        elif rain_prob >= 60:
            return "🌂 Carry umbrella. Rain very likely in next 6-12 hours."
        elif rain_prob >= 40:
            return "☁️ Cloudy skies. Light drizzle possible. Check again later."
        elif humidity > 80 and pressure < 1010:
            return "🌡️ Muggy weather. Rain building up — sense-7 tingling!"
        else:
            return "☀️ Clear skies. Good day for outdoor coding! 😎"
    
    def _default_result(self) -> Dict:
        """Fallback if API fails."""
        return {
            "rain_probability": 0,
            "temperature": 0,
            "humidity": 0,
            "cloud_cover": 0,
            "pressure": 0,
            "wind_speed": 0,
            "factors": {},
            "tip": "❌ Could not fetch data. Check internet connection."
        }
