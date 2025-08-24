from flask import Flask, jsonify, render_template
import random
import time
import threading
from datetime import datetime

app = Flask(__name__)

# Simulated sensor data
garden_data = {
    'soil_moisture': 50.0,  # percentage
    'sunlight': 70.0,       # percentage
    'temperature': 22.0,    # celsius
    'last_updated': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
}

# Thresholds for alerts
ALERT_THRESHOLDS = {
    'soil_moisture': 30.0,  # Water if below this
    'sunlight': 20.0,       # Low light warning
    'temperature': 10.0     # Too cold warning
}

def update_sensor_data():
    """Simulate sensor readings changing over time"""
    while True:
        # Simulate gradual changes
        garden_data['soil_moisture'] = max(10, min(90, 
            garden_data['soil_moisture'] + random.uniform(-5, 5)))
        
        garden_data['sunlight'] = max(0, min(100, 
            garden_data['sunlight'] + random.uniform(-10, 10)))
        
        garden_data['temperature'] = max(5, min(35, 
            garden_data['temperature'] + random.uniform(-2, 2)))
        
        garden_data['last_updated'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Simulate sensor reading interval (3 minutes)
        time.sleep(180)

@app.route('/')
def dashboard():
    """Render the main dashboard"""
    return render_template('dashboard.html')

@app.route('/api/garden-status')
def garden_status():
    """API endpoint to get current garden status"""
    # Calculate alerts
    alerts = []
    if garden_data['soil_moisture'] < ALERT_THRESHOLDS['soil_moisture']:
        alerts.append("Water me! Soil moisture is low.")
    if garden_data['sunlight'] < ALERT_THRESHOLDS['sunlight']:
        alerts.append("Low light detected. Consider moving to a sunnier spot.")
    if garden_data['temperature'] < ALERT_THRESHOLDS['temperature']:
        alerts.append("Too cold! Consider moving to a warmer location.")
    
    return jsonify({
        'sensor_data': garden_data,
        'alerts': alerts,
        'status': 'healthy' if not alerts else 'needs_attention'
    })

if __name__ == '__main__':
    # Start the background thread to simulate sensor updates
    sensor_thread = threading.Thread(target=update_sensor_data, daemon=True)
    sensor_thread.start()
    
    app.run(debug=True)