import sys
import os
from dotenv import load_dotenv
load_dotenv()
from travel_agent import TravelAgent
import itinerary_builder
import google_services
import traffic_analyzer
import crowd_predictor

def print_header():
    print("="*50)
    print("🌍 AI Smart Travel Companion")
    print("="*50)

def explore_mode():
    print("\n🧭 Explore Mode Activated!")
    location = input("Where are you right now? (e.g., Colaba, Mumbai) > ")
    print("\n🔍 Checking smart metrics...")
    
    nearby = google_services.find_nearby(location)
    
    print(f"\nRecommended Nearby Attractions:")
    for place in nearby:
        crowd = crowd_predictor.predict_crowd_level(place, "Now")
        print(f"• {place} - Crowd Level: {crowd['status']} ({crowd['popularity_score']}%)")
        
    print("\n🍽 Smart Food Recommendations:")
    print("• Leopold Cafe ⭐4.5")
    print("• Cafe Mondegar ⭐4.4")

def main():
    print_header()
    print("Welcome to your personal AI trip planner.")
    print("1. Plan a Trip")
    print("2. Explore Mode (What can I do near me right now?)")
    print("3. Exit\n")
    
    choice = input("Enter your choice (1-3): ")
    
    if choice == '2':
        explore_mode()
        sys.exit(0)
    elif choice == '3':
        sys.exit(0)
    elif choice != '1':
        print("Invalid choice.")
        sys.exit(1)

    print("\n--- Plan Your Trip ---")
    destination = input("Destination (e.g., Mumbai): ")
    days = input("Number of days (e.g., 2): ")
    interests = input("Interests (e.g., food, culture, adventure): ")
    budget = input("Budget (low/medium/high): ")
    email = input("Your email address (for summary): ")
    
    print("\n🤖 AI is planning your trip. Please wait...")
    print("• Searching for attractions via Google Places...")
    print("• Analyzing live traffic and crowd popularity...")
    print("• Optimizing route & checking weather forecasts...")
    
    agent = TravelAgent(destination, days, interests, budget)
    structured_plan = agent.generate_plan()
    
    # Build text output
    text_itinerary = itinerary_builder.build_itinerary_text(structured_plan)
    
    print("\n" + text_itinerary)
    
    # Calendar & Email
    # In a real app we'd map `days_list` into Google Calendar Event formats
    google_services.add_to_calendar(structured_plan['days_list'])
    google_services.send_summary_email(email, f"Your {destination} Trip Plan", text_itinerary)
    
    print("\n✅ Done! Have a safe trip!")

if __name__ == "__main__":
    main()
