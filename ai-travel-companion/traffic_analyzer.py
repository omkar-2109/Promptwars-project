import random

def analyze_traffic(origin, destination):
    """
    Simulates Google Maps Directions API traffic levels.
    """
    base_distance_km = random.uniform(1.0, 15.0)
    base_time_mins = int(base_distance_km * random.uniform(3.0, 6.0))
    
    traffic_conditions = ["Light", "Moderate", "Heavy"]
    traffic = random.choice(traffic_conditions)
    
    if traffic == "Heavy":
        time_mins = int(base_time_mins * 1.5)
        alert = f"Heavy traffic detected towards {destination}. Alternative Route Suggested."
    elif traffic == "Moderate":
        time_mins = int(base_time_mins * 1.2)
        alert = None
    else:
        time_mins = base_time_mins
        alert = None
        
    return {
        "distance": f"{base_distance_km:.1f} km",
        "estimated_time_mins": time_mins,
        "traffic_level": traffic,
        "alert": alert
    }
