#!/usr/bin/env python3
"""
Global Air Quality Monitoring System
Main application entry point.
"""
import os
import sys
from dotenv import load_dotenv

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from air_quality.api.routes import AirQualityAPI

# Load environment variables
load_dotenv()

def create_app():
    """Create and configure the Flask application."""
    api = AirQualityAPI()
    return api.app

def main():
    """Main entry point for the application."""
    print("🌍 Starting Global Air Quality Monitoring System...")
    print("📡 Initializing data collectors...")
    print("🗺️  Setting up monitoring dashboard...")
    
    api = AirQualityAPI()
    
    # Get configuration from environment variables
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    print(f"🚀 Dashboard available at: http://{host}:{port}")
    print("📊 API endpoints:")
    print(f"   • http://{host}:{port}/api/air-quality/all")
    print(f"   • http://{host}:{port}/api/locations")
    print(f"   • http://{host}:{port}/api/categories")
    print("💨 Monitoring air quality across the globe...")
    
    api.run(host=host, port=port, debug=debug)

if __name__ == '__main__':
    main()