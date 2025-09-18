"""
Configuration settings for the Air Quality Monitoring System.
"""
import os
from typing import Dict, Any


class Config:
    """Base configuration class."""
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    HOST = os.getenv('FLASK_HOST', '0.0.0.0')
    PORT = int(os.getenv('FLASK_PORT', 5000))
    
    # API Keys
    OPENWEATHERMAP_API_KEY = os.getenv('OPENWEATHERMAP_API_KEY', '')
    
    # Data Collection Settings
    DEFAULT_DATA_COLLECTOR = os.getenv('DEFAULT_DATA_COLLECTOR', 'simulated')
    DATA_REFRESH_INTERVAL = int(os.getenv('DATA_REFRESH_INTERVAL', 300))  # seconds
    
    # Monitoring Locations
    MONITORING_LOCATIONS = [
        {
            'name': 'New York',
            'latitude': 40.7128,
            'longitude': -74.0060,
            'country': 'USA',
            'city': 'New York',
            'state': 'NY'
        },
        {
            'name': 'Los Angeles',
            'latitude': 34.0522,
            'longitude': -118.2437,
            'country': 'USA',
            'city': 'Los Angeles',
            'state': 'CA'
        },
        {
            'name': 'Beijing',
            'latitude': 39.9042,
            'longitude': 116.4074,
            'country': 'China',
            'city': 'Beijing',
            'state': 'Beijing'
        },
        {
            'name': 'London',
            'latitude': 51.5074,
            'longitude': -0.1278,
            'country': 'UK',
            'city': 'London',
            'state': 'England'
        },
        {
            'name': 'Delhi',
            'latitude': 28.7041,
            'longitude': 77.1025,
            'country': 'India',
            'city': 'Delhi',
            'state': 'Delhi'
        },
        {
            'name': 'Tokyo',
            'latitude': 35.6762,
            'longitude': 139.6503,
            'country': 'Japan',
            'city': 'Tokyo',
            'state': 'Tokyo'
        }
    ]
    
    @classmethod
    def get_config_dict(cls) -> Dict[str, Any]:
        """Get configuration as dictionary."""
        return {
            'secret_key': cls.SECRET_KEY,
            'debug': cls.DEBUG,
            'host': cls.HOST,
            'port': cls.PORT,
            'openweathermap_api_key': cls.OPENWEATHERMAP_API_KEY,
            'default_data_collector': cls.DEFAULT_DATA_COLLECTOR,
            'data_refresh_interval': cls.DATA_REFRESH_INTERVAL,
            'monitoring_locations': cls.MONITORING_LOCATIONS
        }


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    SECRET_KEY = os.getenv('SECRET_KEY')  # Must be set in production
    
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY environment variable must be set in production")


class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DEBUG = True


# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}