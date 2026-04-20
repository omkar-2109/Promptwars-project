import os
import json
import requests

def get_attractions(location, interests, weather_data):
    """
    Google Places API Text Search.
    Selects attractions based on location, interests.
    """
    api_key = os.getenv("GOOGLE_PLACES_API_KEY")
    
    # Fallback to mock if missing
    if not api_key:
        print("[Google Services] Using mock attractions due to missing API key.")
        return _mock_get_attractions(location, interests, weather_data)

    query = f"{interests} in {location}" if interests else f"tourist attractions in {location}"
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={query}&key={api_key}"
    
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        if data.get("status") != "OK":
            print(f"[Google Places API Error] Status: {data.get('status')}")
            return _mock_get_attractions(location, interests, weather_data)
        
        places = []
        park_count = 0
        
        for result in data.get("results", [])[:20]: # Increase to top 20 to allow filtering
            status = result.get("business_status", "OPERATIONAL")
            if status != "OPERATIONAL":
                continue
                
            types = result.get("types", [])
            
            # Check park count constraint
            if "park" in types or "natural_feature" in types:
                if park_count >= 1:
                    continue
                park_count += 1
                
            place_type = "indoor"
            if "park" in types or "natural_feature" in types: place_type = "outdoor"
            elif "museum" in types or "art_gallery" in types: place_type = "museum"
            elif "restaurant" in types or "cafe" in types: place_type = "food"
            else: place_type = "outdoor"
            
            places.append({
                "name": result.get("name"),
                "place_id": result.get("place_id"),
                "interest": interests,
                "type": place_type,
                "rating": result.get("rating", str(result.get("rating", 4.0))),
                "address": result.get("formatted_address", f"{result.get('name')}, {location}")
            })
            
            # Stop if we have enough diverse places
            if len(places) >= 10:
                break
            
        if not places:
            return _mock_get_attractions(location, interests, weather_data)
            
        return places
        
    except Exception as e:
        print(f"[Google Places API Error] {e} - falling back to mock.")
        return _mock_get_attractions(location, interests, weather_data)


def find_nearby(current_location):
    """
    Google Places API Nearby Search (using text search).
    """
    api_key = os.getenv("GOOGLE_PLACES_API_KEY")
    if not api_key:
        print("[Google Services] Using mock nearby due to missing API key.")
        return _mock_find_nearby(current_location)

    query = f"attractions near {current_location}"
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={query}&key={api_key}"
    
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        if data.get("status") != "OK":
            return _mock_find_nearby(current_location)
            
        results = data.get("results", [])[:3]
        return [f"{r.get('name')} (Rating: {r.get('rating', 'N/A')})" for r in results]
    except Exception as e:
        print(f"[Google Places API Error] {e} - falling back to mock.")
        return _mock_find_nearby(current_location)

def get_place_info(place_id, place_name):
    """
    Fetches the place details to get a 1-2 line editorial summary.
    """
    api_key = os.getenv("GOOGLE_PLACES_API_KEY")
    if not api_key or not place_id:
        return f"A highly-rated destination worth visiting while exploring."
    
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=editorial_summary&key={api_key}"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        
        if data.get("status") == "OK":
            result = data.get("result", {})
            if "editorial_summary" in result and "overview" in result["editorial_summary"]:
                return result["editorial_summary"]["overview"]
        
        return f"A highly-rated destination worth visiting."
    except Exception as e:
        print(f"[Google Places Detail API Error] {e}")
        return f"A highly-rated destination worth visiting."


def _mock_get_attractions(location, interests, weather_data):
    """Fallback logic from previous version"""
    places_db = {
        "Mumbai": [
            {"name": "Gateway of India", "interest": "culture", "type": "outdoor", "rating": 4.7},
            {"name": "Elephanta Caves", "interest": "culture", "type": "outdoor", "rating": 4.5},
            {"name": "Prince of Wales Museum", "interest": "culture", "type": "museum", "rating": 4.6},
            {"name": "Marine Drive", "interest": "nature", "type": "outdoor", "rating": 4.8},
            {"name": "Colaba Causeway Market", "interest": "shopping", "type": "outdoor", "rating": 4.3},
            {"name": "Sanjay Gandhi National Park", "interest": "adventure", "type": "outdoor", "rating": 4.4},
            {"name": "Leopold Cafe", "interest": "food", "type": "food", "rating": 4.5},
            {"name": "Cafe Mondegar", "interest": "food", "type": "food", "rating": 4.4},
            {"name": "Bademiya", "interest": "food", "type": "food", "rating": 4.6},
            {"name": "Taj Mahal Palace Hotel", "interest": "culture", "type": "indoor", "rating": 4.9}
        ]
    }
    
    city_places = places_db.get(location, [
        {"name": f"Famous Point in {location}", "interest": "culture", "type": "outdoor", "rating": 4.5},
        {"name": f"{location} Museum", "interest": "culture", "type": "museum", "rating": 4.4},
        {"name": f"{location} Bistro", "interest": "food", "type": "food", "rating": 4.6},
        {"name": f"{location} Park", "interest": "nature", "type": "outdoor", "rating": 4.7}
    ])
    
    interest_list = [i.strip().lower() for i in interests.split(',')]
    filtered_places = []
    
    for place in city_places:
        if any(interest in place["interest"].lower() for interest in interest_list) or place["type"] == "food":
             filtered_places.append(place)
             
    if not filtered_places:
        filtered_places = city_places
        
    return filtered_places

def _mock_find_nearby(current_location):
    mock_nearby_db = {
        "Colaba": ["Gateway of India (400m)", "Taj Mahal Palace Hotel", "Colaba Causeway Market"],
        "Marine Drive": ["Chowpatty Beach", "Taraporewala Aquarium", "Wankhede Stadium"]
    }
    
    return mock_nearby_db.get(current_location, [
        f"Central Cafe near {current_location} (200m)",
        f"Local Plaza near {current_location} (500m)"
    ])

def add_to_calendar(itinerary_days):
    """
    Mock Google Calendar API.
    Simulates adding events.
    """
    print("\n[Google Services] Connecting to Google Calendar API...")
    event_count = 0
    for day in itinerary_days:
         event_count += len(day.keys())
    
    print(f"[Google Services] Successfully created {event_count} events on your Google Calendar.")

def send_summary_email(email_address, subject, text_body):
    """
    Mock Gmail API.
    Simulates sending an email.
    """
    print(f"\n[Google Services] Sending email to {email_address} via Gmail API...")
    print(f"[Google Services] Email Sent! Subject: {subject}")

def get_air_quality(location):
    """
    Integrates GCP Air Quality API.
    Geocodes the location, then looks up the air quality current conditions.
    """
    api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    if not api_key:
        return {"aqi": "42", "category": "Good (Mock)", "dominant_pollutant": "pm25"}
        
    geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={location}&key={api_key}"
    try:
        geo_res = requests.get(geocode_url, timeout=5).json()
        if geo_res.get("status") == "OK":
            coords = geo_res["results"][0]["geometry"]["location"]
            
            aq_url = f"https://airquality.googleapis.com/v1/currentConditions:lookup?key={api_key}"
            payload = {"location": coords}
            aq_res = requests.post(aq_url, json=payload, timeout=5).json()
            
            if "indexes" in aq_res:
                index = aq_res["indexes"][0]
                return {
                    "aqi": index.get("aqiDisplay", "N/A"),
                    "category": index.get("category", "Unknown"),
                    "dominant_pollutant": index.get("dominantPollutant", "N/A")
                }
    except Exception as e:
        print(f"[GCP Air Quality API Error] {e} - falling back to mock.")
        pass
    
    return {"aqi": "42", "category": "Good (Mock)", "dominant_pollutant": "pm25"}
