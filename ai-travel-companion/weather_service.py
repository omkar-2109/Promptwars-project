import random
import os
import requests

def check_weather(location):
    """
    OpenWeather API integration.
    Returns weather condition and temperature.
    """
    api_key = os.getenv("OPENWEATHER_API_KEY")
    
    # Fallback to mock if no key is set
    if not api_key:
        conditions = ["Clear", "Sunny", "Cloudy", "Rain"]
        seed_num = sum(ord(c) for c in location)
        random.seed(seed_num)
        condition = random.choice(conditions)
        temp = random.randint(22, 35) # Celcius
        return {
            "condition": condition,
            "temperature": temp,
            "is_raining": condition == "Rain"
        }
        
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        condition = data["weather"][0]["main"]
        temp = data["main"]["temp"]
        
        return {
            "condition": condition,
            "temperature": round(temp),
            "is_raining": condition.lower() in ["rain", "drizzle", "thunderstorm"]
        }
    except Exception as e:
        print(f"[Weather API Error] {e} - falling back to mock.")
        return {
            "condition": "Cloudy",
            "temperature": 25,
            "is_raining": False
        }

def adjust_for_weather(plan_items, weather_data):
    """
    Adjusts the plan if the weather is adverse.
    For simplicity, if it's raining, we swap outdoor with indoor.
    """
    if weather_data["is_raining"]:
        return [item for item in plan_items if item.get("type") in ["indoor", "museum", "food", "cafe"]]
    return plan_items
