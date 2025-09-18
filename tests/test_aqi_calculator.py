"""
Tests for AQI Calculator functionality.
"""
import pytest
import sys
import os
from datetime import datetime

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))

from air_quality.core.models import Location, Pollutant, PollutantReading, AQICategory
from air_quality.core.aqi_calculator import AQICalculator


class TestAQICalculator:
    """Test cases for AQI Calculator."""
    
    def test_calculate_pm25_aqi_good(self):
        """Test PM2.5 AQI calculation for good air quality."""
        aqi = AQICalculator.calculate_individual_aqi(Pollutant.PM2_5, 10.0)
        assert 0 <= aqi <= 50
        
    def test_calculate_pm25_aqi_moderate(self):
        """Test PM2.5 AQI calculation for moderate air quality."""
        aqi = AQICalculator.calculate_individual_aqi(Pollutant.PM2_5, 25.0)
        assert 51 <= aqi <= 100
        
    def test_calculate_pm25_aqi_unhealthy(self):
        """Test PM2.5 AQI calculation for unhealthy air quality."""
        aqi = AQICalculator.calculate_individual_aqi(Pollutant.PM2_5, 100.0)
        assert 151 <= aqi <= 200
        
    def test_calculate_multiple_pollutants(self):
        """Test AQI calculation with multiple pollutants."""
        readings = [
            PollutantReading(
                pollutant=Pollutant.PM2_5,
                concentration=25.0,
                unit="μg/m³",
                timestamp=datetime.now()
            ),
            PollutantReading(
                pollutant=Pollutant.O3,
                concentration=0.06,
                unit="ppm",
                timestamp=datetime.now()
            ),
            PollutantReading(
                pollutant=Pollutant.NO2,
                concentration=75,
                unit="μg/m³",
                timestamp=datetime.now()
            )
        ]
        
        aqi, dominant_pollutant = AQICalculator.calculate_aqi(readings)
        
        assert aqi > 0
        assert dominant_pollutant in [Pollutant.PM2_5, Pollutant.O3, Pollutant.NO2]
        
    def test_create_air_quality_reading(self):
        """Test creating a complete air quality reading."""
        location = Location("Test City", 40.7128, -74.0060, "USA")
        
        readings = [
            PollutantReading(
                pollutant=Pollutant.PM2_5,
                concentration=15.0,
                unit="μg/m³",
                timestamp=datetime.now()
            )
        ]
        
        air_quality = AQICalculator.create_air_quality_reading(
            location=location,
            pollutant_readings=readings,
            source="Test"
        )
        
        assert air_quality.location.name == "Test City"
        assert air_quality.aqi > 0
        assert air_quality.category is not None
        assert len(air_quality.readings) == 1
        
    def test_aqi_categories(self):
        """Test AQI category classification."""
        # Test each category range
        test_cases = [
            (25, AQICategory.GOOD),
            (75, AQICategory.MODERATE),
            (125, AQICategory.UNHEALTHY_SENSITIVE),
            (175, AQICategory.UNHEALTHY),
            (250, AQICategory.VERY_UNHEALTHY),
            (350, AQICategory.HAZARDOUS)
        ]
        
        for aqi_value, expected_category in test_cases:
            category = AQICategory.from_aqi(aqi_value)
            assert category == expected_category, f"AQI {aqi_value} should be {expected_category.label}"
            
    def test_edge_cases(self):
        """Test edge cases and boundary conditions."""
        # Test zero concentration
        aqi = AQICalculator.calculate_individual_aqi(Pollutant.PM2_5, 0.0)
        assert aqi == 0
        
        # Test very high concentration
        aqi = AQICalculator.calculate_individual_aqi(Pollutant.PM2_5, 1000.0)
        assert aqi == 500  # Should cap at 500
        
        # Test empty readings list
        aqi, dominant = AQICalculator.calculate_aqi([])
        assert aqi == 0
        assert dominant == Pollutant.PM2_5  # Default


if __name__ == '__main__':
    pytest.main([__file__])