"""
Sense-7: Rain Prediction Engine
Built by Shivay Singh (12-year-old founder)
Theme: Dark (#0a0e17) + Gold (#d4af37)
"""

import streamlit as st
import requests
from datetime import datetime
from src.predictor import RainPredictor

# ─────────────────────────────────────────────────────────────
# PAGE CONFIG (Mobile-first)
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Sense-7 | Rain Prediction",
    page_icon="🌧️",
    layout="centered",  # Mobile-friendly
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────────────────────────
# CUSTOM CSS — Dark + Gold Theme
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background-color: #0a0e17;
        color: #d4af37;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #d4af37 !important;
        font-family: 'Courier New', monospace;
    }
    
    /* Buttons */
    .stButton>button {
        background-color: #d4af37;
        color: #0a0e17;
        border-radius: 10px;
        border: none;
        font-weight: bold;
        width: 100%;
        padding: 15px;
        font-size: 16px;
    }
    .stButton>button:hover {
        background-color: #f4d03f;
        color: #0a0e17;
    }
    
    /* Metric cards */
    .metric-card {
        background-color: #1a1f2e;
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #d4af37;
        margin: 10px 0;
    }
    
    /* Rain animation text */
    .rain-text {
        font-size: 24px;
        color: #00d4aa;
        text-align: center;
        font-weight: bold;
        padding: 20px;
    }
    
    /* Location input */
    .stTextInput>div>div>input {
        background-color: #1a1f2e;
        color: #d4af37;
        border: 2px solid #d4af37;
        border-radius: 10px;
    }
    
    /* Success/Error messages */
    .stSuccess {
        background-color: #1e3d2f !important;
        color: #2ed573 !important;
    }
    .stError {
        background-color: #3d1e1e !important;
        color: #ff4757 !important;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────
st.title("🌧️ Sense-7")
st.markdown("*The 7th Sense: Rain Prediction Engine*")
st.markdown("---")

# ─────────────────────────────────────────────────────────────
# INPUT SECTION
# ─────────────────────────────────────────────────────────────
st.subheader("📍 Your Location")

# Popular Indian cities for quick select
CITIES = {
    "Kanpur": (26.4499, 80.3319),
    "Delhi": (28.6139, 77.2090),
    "Mumbai": (19.0760, 72.8777),
    "Kolkata": (22.5726, 88.3639),
    "Chennai": (13.0827, 80.2707),
    "Bengaluru": (12.9716, 77.5946),
    "Hyderabad": (17.3850, 78.4867),
    "Lucknow": (26.8467, 80.9462),
}

city_choice = st.selectbox("Quick select:", list(CITIES.keys()) + ["Custom Location"])
if city_choice == "Custom Location":
    lat = st.number_input("Latitude:", value=26.4499, format="%.4f")
    lon = st.number_input("Longitude:", value=80.3319, format="%.4f")
else:
    lat, lon = CITIES[city_choice]
    st.success(f"Selected: {city_choice} ({lat}, {lon})")

# ─────────────────────────────────────────────────────────────
# PREDICTION SECTION
# ─────────────────────────────────────────────────────────────
if st.button("🌧️ ACTIVATE 7TH SENSE"):
    with st.spinner("Consulting the rain gods... ⛈️"):
        try:
            # Fetch weather data
            url = (
                f"https://api.open-meteo.com/v1/forecast?"
                f"latitude={lat}&longitude={lon}"
                f"&hourly=temperature_2m,relativehumidity_2m,precipitation_probability,"
                f"surface_pressure,cloudcover,windspeed_10m"
                f"&forecast_days=3&timezone=auto"
            )
            response = requests.get(url, timeout=10)
            data = response.json()
            
            # Initialize predictor
            predictor = RainPredictor()
            result = predictor.predict_rain(data)
            
            # ─────────────────────────────────────────────────
            # DISPLAY RESULTS
            # ─────────────────────────────────────────────────
            st.markdown("---")
            st.subheader("📊 7th Sense Report")
            
            # Main prediction
            rain_prob = result['rain_probability']
            
            if rain_prob >= 70:
                emoji = "🌧️🌧️🌧️"
                verdict = "HEAVY RAIN LIKELY!"
                color = "#ff4757"
            elif rain_prob >= 40:
                emoji = "🌦️"
                verdict = "RAIN POSSIBLE"
                color = "#ffa502"
            else:
                emoji = "☀️"
                verdict = "CLEAR SKIES"
                color = "#2ed573"
            
            # Animated result box
            st.markdown(f"""
            <div class="metric-card" style="border-left-color: {color};">
                <div style="font-size: 48px; text-align: center;">{emoji}</div>
                <div style="font-size: 28px; text-align: center; color: {color}; font-weight: bold;">
                    {verdict}
                </div>
                <div style="font-size: 20px; text-align: center; color: #d4af37;">
                    Confidence: {rain_prob}%
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Detailed metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("🌡️ Temp", f"{result['temperature']}°C")
            with col2:
                st.metric("💧 Humidity", f"{result['humidity']}%")
            with col3:
                st.metric("☁️ Clouds", f"{result['cloud_cover']}%")
            
            # 7th Sense tip (Dr. Titan style)
            st.info(f"💡 **Sense-7 Tip:** {result['tip']}")
            
            # Confidence bar
            st.progress(rain_prob / 100)
            
            # Timestamp
            st.caption(f"Last updated: {datetime.now().strftime('%H:%M:%S')}")
            
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.info("Check internet connection and try again!")

# ─────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #d4af37; opacity: 0.7;">
    <p>Built by Shivay Singh (12) 🐍</p>
    <p>Powered by Open-Meteo API + Python</p>
    <p style="font-size: 12px;">Sense-7: Validated by real rain since 2026 🌧️</p>
</div>
""", unsafe_allow_html=True)
