import random

def predict_crowd_level(location_name, time_of_day):
    """
    Simulates predicting crowd level based on location and time.
    Uses Google Places Popular Times concepts.
    """
    # Create a deterministic mock based on time and name
    seed_idx = len(location_name) + len(time_of_day)
    random.seed(seed_idx)
    
    # 0 to 100
    popularity = random.randint(20, 95)
    
    if popularity > 70:
        status = "Very Crowded"
    elif popularity > 40:
        status = "Moderately Busy"
    else:
        status = "Less Crowded"
        
    return {
        "popularity_score": popularity,
        "status": status,
        "recommended_visit_delay_hours": 2 if popularity > 70 else 0
    }

def get_best_time_to_visit(location_name):
    """
    Returns the ideal time to visit based on "historical" mock data.
    """
    times = ["8:00 AM - 10:00 AM", "2:00 PM - 4:00 PM", "Sunset (6:30 PM)", "8:00 PM - 10:00 PM"]
    return random.choice(times)
