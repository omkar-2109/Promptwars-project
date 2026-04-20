import google_services
import weather_service
import traffic_analyzer
import crowd_predictor

class TravelAgent:
    def __init__(self, destination, days, interests, budget):
        self.destination = destination
        self.days = int(days)
        self.interests = interests
        self.budget = budget

    def generate_plan(self):
        """
        Core reasoning function. Fetches logic, creates a structured itinerary.
        """
        # 1. Check weather and air quality (GCP API)
        weather = weather_service.check_weather(self.destination)
        weather['air_quality'] = google_services.get_air_quality(self.destination)
        
        # 2. Get places based on interests
        all_places = google_services.get_attractions(self.destination, self.interests, weather)
        
        # 3. Filter weather (if raining, favor indoors)
        applicable_places = weather_service.adjust_for_weather(all_places, weather)
        
        # Filter into types
        foods = [p for p in applicable_places if p['type'] == 'food']
        attractions = [p for p in applicable_places if p['type'] != 'food']
        
        days_list = []
        
        import urllib.parse
        
        # Define diverse fallbacks to prevent 'Local Park' repeating endlessly
        fallback_attractions = [
            {"name": "Local Park", "rating": "4.0"}, 
            {"name": "City Museum", "rating": "4.2"}, 
            {"name": "Downtown Plaza", "rating": "4.5"}, 
            {"name": "Botanical Gardens", "rating": "4.3"}
        ]
        fallback_foods = [
            {"name": "Local Restaurant", "rating": "4.0"}, 
            {"name": "Popular Cafe", "rating": "4.4"}, 
            {"name": "Bistro Downtown", "rating": "4.6"}
        ]
        
        # Assign slots for each day
        for d in range(self.days):
            day_plan = {}
            current_location = None
            
            slots = ["Morning", "Lunch", "Afternoon", "Evening"]
            for slot in slots:
                if slot == "Lunch":
                    # Pick a food place
                    if foods:
                        place = foods.pop(0)
                        # don't append right away to avoid immediate repeats if possible
                        foods.append(place)
                    else:
                        place = fallback_foods.pop(0)
                        fallback_foods.append(place)
                else:
                    if attractions:
                        place = attractions.pop(0)
                        attractions.append(place)
                    else:
                        place = fallback_attractions.pop(0)
                        fallback_attractions.append(place)
                
                place_name = place['name']
                
                # Check crowd
                crowd = crowd_predictor.predict_crowd_level(place_name, slot)
                
                # If too crowded, we could re-arrange, but we just annotate for now
                if crowd["status"] == "Very Crowded" and len(attractions) > 1 and slot != "Lunch":
                    # Swap with another attraction
                    next_place = attractions.pop(0)
                    attractions.append(place)
                    place = next_place
                    place_name = place['name']
                    crowd = crowd_predictor.predict_crowd_level(place_name, slot)
                
                # Check traffic from last location
                traffic = None
                if current_location:
                    traffic = traffic_analyzer.analyze_traffic(current_location, place_name)
                    
                map_query = urllib.parse.quote(f"{place_name} {self.destination}")
                map_url = f"https://www.google.com/maps/search/?api=1&query={map_query}"
                
                # Fetch 1-2 line summary
                place_id = place.get('place_id')
                summary = google_services.get_place_info(place_id, place_name)
                
                day_plan[slot] = {
                    "place": place_name,
                    "summary": summary,
                    "rating": place.get('rating', 'N/A'),
                    "map_url": map_url,
                    "crowd": crowd,
                    "traffic": traffic,
                    "weather": weather if slot in ["Morning", "Afternoon"] else None
                }
                
                current_location = place_name
                
            days_list.append(day_plan)

        return {
            "destination": self.destination,
            "days": self.days,
            "budget": self.budget,
            "days_list": days_list
        }
