"""
Flask API routes for air quality monitoring system.
"""
from flask import Flask, jsonify, request, render_template
from datetime import datetime
from typing import List, Dict, Any
from ..core.models import Location, AQICategory
from ..data.collectors import DataCollectorFactory


class AirQualityAPI:
    """Air Quality Monitoring API."""
    
    def __init__(self):
        self.app = Flask(__name__, 
                        template_folder='../../../../templates',
                        static_folder='../../../../static')
        self.collector = DataCollectorFactory.create_collector("simulated")
        self.setup_routes()
        
        # Sample locations for demonstration
        self.sample_locations = [
            Location("New York", 40.7128, -74.0060, "USA", "New York", "NY"),
            Location("Los Angeles", 34.0522, -118.2437, "USA", "Los Angeles", "CA"),
            Location("Beijing", 39.9042, 116.4074, "China", "Beijing", "Beijing"),
            Location("London", 51.5074, -0.1278, "UK", "London", "England"),
            Location("Delhi", 28.7041, 77.1025, "India", "Delhi", "Delhi"),
            Location("Tokyo", 35.6762, 139.6503, "Japan", "Tokyo", "Tokyo")
        ]
    
    def setup_routes(self):
        """Setup all API routes."""
        
        @self.app.route('/')
        def dashboard():
            """Main dashboard page."""
            return render_template('dashboard.html')
        
        @self.app.route('/api/locations')
        def get_locations():
            """Get list of monitored locations."""
            locations = []
            for loc in self.sample_locations:
                locations.append({
                    'name': loc.name,
                    'latitude': loc.latitude,
                    'longitude': loc.longitude,
                    'country': loc.country,
                    'city': loc.city,
                    'state': loc.state
                })
            return jsonify(locations)
        
        @self.app.route('/api/air-quality/<location_name>')
        def get_air_quality(location_name):
            """Get current air quality for a specific location."""
            location = next((loc for loc in self.sample_locations 
                           if loc.name.lower() == location_name.lower()), None)
            
            if not location:
                return jsonify({'error': 'Location not found'}), 404
            
            try:
                reading = self.collector.fetch_current_data(location)
                
                return jsonify({
                    'location': {
                        'name': reading.location.name,
                        'latitude': reading.location.latitude,
                        'longitude': reading.location.longitude,
                        'country': reading.location.country
                    },
                    'aqi': reading.aqi,
                    'category': {
                        'name': reading.category.label,
                        'color': reading.category.color
                    },
                    'dominant_pollutant': reading.dominant_pollutant.value,
                    'readings': [
                        {
                            'pollutant': r.pollutant.value,
                            'concentration': r.concentration,
                            'unit': r.unit
                        } for r in reading.readings
                    ],
                    'timestamp': reading.timestamp.isoformat(),
                    'source': reading.source
                })
                
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/air-quality/all')
        def get_all_air_quality():
            """Get current air quality for all monitored locations."""
            results = []
            
            for location in self.sample_locations:
                try:
                    reading = self.collector.fetch_current_data(location)
                    
                    results.append({
                        'location': {
                            'name': reading.location.name,
                            'latitude': reading.location.latitude,
                            'longitude': reading.location.longitude,
                            'country': reading.location.country
                        },
                        'aqi': reading.aqi,
                        'category': {
                            'name': reading.category.label,
                            'color': reading.category.color
                        },
                        'dominant_pollutant': reading.dominant_pollutant.value,
                        'timestamp': reading.timestamp.isoformat()
                    })
                    
                except Exception as e:
                    results.append({
                        'location': {'name': location.name},
                        'error': str(e)
                    })
            
            return jsonify(results)
        
        @self.app.route('/api/categories')
        def get_aqi_categories():
            """Get AQI category information."""
            categories = []
            for category in AQICategory:
                categories.append({
                    'name': category.label,
                    'min_aqi': category.min_aqi,
                    'max_aqi': category.max_aqi,
                    'color': category.color
                })
            return jsonify(categories)
        
        @self.app.route('/api/health')
        def health_check():
            """Health check endpoint."""
            return jsonify({
                'status': 'healthy',
                'timestamp': datetime.now().isoformat(),
                'version': '1.0.0'
            })
    
    def run(self, host='0.0.0.0', port=5000, debug=True):
        """Run the Flask application."""
        self.app.run(host=host, port=port, debug=debug)