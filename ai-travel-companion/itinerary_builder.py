def build_itinerary_text(itinerary_data):
    """
    Converts structured itinerary data from travel_agent into readable text.
    """
    lines = []
    
    lines.append("="*40)
    lines.append(f"🌍 Your Smart Travel Itinerary: {itinerary_data['destination']}")
    lines.append(f"📅 Trip Duration: {itinerary_data['days']} days")
    lines.append(f"💰 Budget: {itinerary_data['budget'].title()}")
    lines.append("="*40)
    
    for day_id, day_plan in enumerate(itinerary_data['days_list'], 1):
        lines.append(f"\nDay {day_id} Plan")
        lines.append("-" * 20)
        
        for slot in ["Morning", "Lunch", "Afternoon", "Evening"]:
            if slot in day_plan:
                activity = day_plan[slot]
                lines.append(f"{slot}:")
                lines.append(f"📍 {activity['place']} (Rating: ⭐{activity['rating']})")
                if 'map_url' in activity:
                    lines.append(f"   🗺️ Map: {activity['map_url']}")
                if activity.get('summary'):
                    lines.append(f"   ℹ️ Info: {activity['summary']}")
                
                # Add insights if present
                if activity.get('weather'):
                    lines.append(f"   🌤 Weather: {activity['weather']['condition']} ({activity['weather']['temperature']}°C)")
                    if activity['weather'].get('air_quality'):
                        aq = activity['weather']['air_quality']
                        lines.append(f"   🍃 Air Quality: {aq.get('category')} (AQI: {aq.get('aqi')})")
                if 'crowd' in activity:
                    crowd_info = activity['crowd']
                    lines.append(f"   👥 Crowd Prediction: {crowd_info['status']} ({crowd_info['popularity_score']}%)")
                if 'traffic' in activity and activity['traffic']:
                     traffic_info = activity['traffic']
                     lines.append(f"   🚗 Traffic from previous: {traffic_info['traffic_level']} ({traffic_info['estimated_time_mins']} mins)")
                     if traffic_info.get('alert'):
                         lines.append(f"   ⚠️ {traffic_info['alert']}")
                         
                lines.append("")
                
    return "\n".join(lines)
