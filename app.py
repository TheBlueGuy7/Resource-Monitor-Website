from flask import Flask, render_template, jsonify
import psutil
import os
import requests
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

# Pterodactyl API configuration
PTERODACTYL_URL = os.getenv('PTERODACTYL_URL')
PTERODACTYL_API_KEY = os.getenv('PTERODACTYL_API_KEY')

def get_system_stats():
    """Get system statistics including CPU, RAM, and disk usage."""
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    return {
        'cpu': {
            'percent': cpu_percent,
            'cores': psutil.cpu_count()
        },
        'memory': {
            'total': memory.total,
            'used': memory.used,
            'free': memory.available,
            'percent': memory.percent
        },
        'disk': {
            'total': disk.total,
            'used': disk.used,
            'free': disk.free,
            'percent': disk.percent
        }
    }

def get_pterodactyl_servers():
    """Get list of Pterodactyl servers."""
    if not PTERODACTYL_URL or not PTERODACTYL_API_KEY:
        print("Pterodactyl configuration missing")
        return []
    
    headers = {
        'Authorization': f'Bearer {PTERODACTYL_API_KEY}',
        'Accept': 'application/json'
    }
    
    try:
        print(f"Fetching servers from: {PTERODACTYL_URL}/api/client")
        response = requests.get(f'{PTERODACTYL_URL}/api/client', headers=headers)
        print(f"Response status code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Received {len(data.get('data', []))} servers")
            return data.get('data', [])
        print(f"Error response: {response.text}")
        return []
    except Exception as e:
        print(f"Error fetching Pterodactyl servers: {e}")
        return []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/system-stats')
def system_stats():
    return jsonify(get_system_stats())

@app.route('/api/pterodactyl-servers')
def pterodactyl_servers():
    return jsonify(get_pterodactyl_servers())

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 