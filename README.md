# 🌧️ Sense-7

**The 7th Sense: Rain Prediction Engine**

[![Python](https://img.shields.io/badge/Python-3.10%2B-d4af37)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-ff4b4b)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue)](LICENSE)
[![Author](https://img.shields.io/badge/Author-Shivay%20Singh%20(12)-2ed573)](https://github.com/singhamit30564-ux)
[![Theme](https://img.shields.io/badge/Theme-Dark%20%2B%20Gold-0a0e17)](https://github.com)

> *"Sense-7: Validated by real rain since 2026"* 🌧️

---

## 🌟 About Sense-7

A **rain prediction app** built with Streamlit and Python. Uses live weather data + a custom weighted algorithm to forecast rain probability for any location.

**The Story:** I once predicted rain using my "7th Sense" — and it actually rained! Now that sense is coded into an app. 🧠⛈️

**Vision:** Free weather intelligence for every village farmer and student in India. 🇮🇳

---

## 🎯 Features

| Feature | Description |
|---------|-------------|
| 📍 **Location-Based** | 10+ Indian cities quick-select + custom coordinates |
| 🌡️ **Real-Time Data** | Open-Meteo API (free, no API key needed) |
| 🧮 **Custom Algorithm** | Weighted factors: humidity, pressure, clouds, wind |
| 📊 **Confidence Score** | 0-100% rain probability with visual progress bar |
| 💡 **Smart Tips** | Contextual advice — umbrella? outdoor coding? |
| 🎨 **Dark + Gold Theme** | `#0a0e17` background + `#d4af37` accents |
| 📱 **Mobile-First** | Works on phones, tablets, desktops |
| 🛡️ **Patent-Protected** | Apache-2.0 — free to use, legally safe |

---

## 🚀 Quick Start

```bash
# Clone
git clone https://github.com/singhamit30564-ux/Sense-7.git
cd Sense-7

# Install dependencies
pip install -r requirements.txt

# Run locally
streamlit run app.py

# 🧮 Prediction Logic
Rain Probability =  (Humidity × 0.35)
 
(Cloud Cover × 0.25)
 
(Air Pressure × 0.20)
 
(API Forecast × 0.15)
 
(Wind Speed × 0.05)

| Factor | Weight | Why It Matters |
|--------|--------|----------------|
| 🌡️ **Humidity** | 35% | >70% humidity = rain very likely |
| ☁️ **Cloud Cover** | 25% | Dense clouds = moisture in sky |
| 🌀 **Air Pressure** | 20% | <1010 hPa = storm system approaching |
| 📡 **API Data** | 15% | Open-Meteo forecast blended in |
| 💨 **Wind Speed** | 5% | High wind + other factors = storm front |

**All scores are 0-100, weighted-averaged, then clamped to valid range.**
# 📂 Project Structure
Sense-7/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── README.md           # This file
├── src/
│   ├── __init__.py
│   ├── predictor.py    # Rain prediction algorithm
│   └── weather_api.py  # Open-Meteo API wrapper
├── .streamlit/
│   └── config.toml     # Dark theme configuration
└── NOTICE              # Apache-2.0 attribution file

