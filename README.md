<div align="center">
  
# 🌍 AI Smart Travel Companion
**Your AI-powered passport to seamless itineraries, crowd predictions, and dynamic weather routing.**

[![Python Badge](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff&style=for-the-badge)](https://python.org/)
[![Flask Badge](https://img.shields.io/badge/Flask-000?logo=flask&logoColor=fff&style=for-the-badge)](https://flask.palletsprojects.com/)
[![Google Cloud](https://img.shields.io/badge/GoogleCloud-%234285F4.svg?style=for-the-badge&logo=google-cloud&logoColor=white)](https://cloud.google.com/)

</div>

---

## ✨ Overview

**AI Smart Travel Companion** is a highly interactive, full-stack travel planner that bridges intelligent backend decision-making with a stunning "glassmorphic" web interface. 

Instead of spending hours researching locations, comparing Google Maps, and checking weather reports, simply tell the AI where you want to go and what you like. Within seconds, it orchestrates a complete, multi-day itinerary factoring in live traffic, crowd congestion, local weather, and GCP air quality index.

## 🚀 Key Features

- **⚡ 3-Second Itineraries**: Generate logical, perfectly paced daily roadmaps instantly.
- **🏢 Deep Google Maps Integration**: Cross-references venues via *Google Places API*, filters out temporarily closed businesses, and generates live direct 1-click Google Maps routing links.
- **🌦️ Live Environment Sync**: Adapts on the fly to global weather patterns (via OpenWeather) and retrieves live AQI/pollutant data using the **GCP Air Quality API**.
- **🚦 AI Crowd Predictions**: Simulates crowd capacities so you know exactly when a location is "Very Crowded" or "Ideal".
- **💎 Interactive UI**: Modern, fully-responsive web application featuring animated background blobs, Multi-Select Toggle Chips, and sleek Glassmorphism design elements.

---

## 🛠️ Technology Stack

- **Backend core**: Python 3, Flask, `requests`, `python-dotenv`
- **Frontend architecture**: Native HTML5, CSS3, Vanilla JavaScript ES6
- **Integrations**: 
  - Google Places API (Text Search & Place Details)
  - Google Maps Geocoding API
  - Google Cloud Environment (Air Quality) API
  - OpenWeather API

---

## ⚙️ Installation & Setup

### 1. Clone & Setup Environment
```bash
git clone https://github.com/yourusername/ai-travel-companion.git
cd ai-travel-companion
```

### 2. Install Dependencies
Make sure you have Python installed, then install the required dependencies:
```bash
pip install -r requirements.txt
```

### 3. API Keys (.env)
Create a `.env` file in the root directory and populate it with your actual API keys:
```ini
GOOGLE_MAPS_API_KEY="your_google_maps_api_key_here"
GOOGLE_PLACES_API_KEY="your_google_places_api_key_here"
OPENWEATHER_API_KEY="your_openweather_api_key_here"
```
> **Note**: Ensure the *Places API*, *Geocoding API*, and *Air Quality API* are enabled in your Google Cloud Console.

### 4. Lift Off! 🚀
Run the Python Flask server:
```bash
python app.py
```
Open your web browser and navigate to: **`http://localhost:8080`**

---

## 🏗️ Project Architecture
```text
ai-travel-companion/
├── app.py                   # Main Flask Route Handler
├── travel_agent.py          # Core AI Itinerary Generator Logic
├── google_services.py       # Interfaces with Google Maps/Places/AQI APIs
├── weather_service.py       # Interfaces with OpenWeather
├── itinerary_builder.py     # String manipulation/formatting for console fallbacks
├── .env                     # Secrets and API keys
├── templates/
│   ├── landing.html         # Premium Product Landing Page
│   └── dashboard.html       # Dynamic Dashboard & Form Input
└── static/
    ├── app.js               # Frontend fetch logic & timeline DOM rendering
    └── style.css            # Glassmorphism design system & UI responses
```

---

<div align="center">
  <i>Built with ❤️ for hassle-free travel.</i>
</div>
