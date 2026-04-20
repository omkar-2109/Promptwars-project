import os
from dotenv import load_dotenv
load_dotenv()
from flask import Flask, render_template, request, jsonify
from travel_agent import TravelAgent
import google_services

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('landing.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/plan', methods=['POST'])
def generate_plan():
    data = request.json
    destination = data.get('destination', 'Mumbai')
    days = int(data.get('days', 2))
    interests = data.get('interests', 'culture, food')
    budget = data.get('budget', 'medium')
    email = data.get('email', '')

    # Initialize agent
    agent = TravelAgent(destination, days, interests, budget)
    structured_plan = agent.generate_plan()
    
    # Mocking Calendar / Email triggers to keep console logs intact
    if email:
        google_services.add_to_calendar(structured_plan['days_list'])
        google_services.send_summary_email(email, f"Your {destination} Trip Plan", "Check console for output!")
        
    return jsonify({"status": "success", "data": structured_plan})

@app.route('/api/explore', methods=['POST'])
def explore_nearby():
    data = request.json
    location = data.get('location', 'Mumbai')
    nearby = google_services.find_nearby(location)
    return jsonify({"status": "success", "data": nearby})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)
