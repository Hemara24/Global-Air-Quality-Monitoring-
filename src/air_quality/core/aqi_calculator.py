"""
AQI (Air Quality Index) calculation engine supporting multiple standards.
"""
from typing import Dict, List, Tuple, Optional
from .models import Pollutant, PollutantReading, AirQualityReading, Location
from datetime import datetime


class AQICalculator:
    """Calculate AQI values for different pollutants using EPA standards."""
    
    # EPA AQI Breakpoints for different pollutants
    # Format: {pollutant: [(C_low, C_high, I_low, I_high), ...]}
    EPA_BREAKPOINTS = {
        Pollutant.PM2_5: [
            (0.0, 12.0, 0, 50),
            (12.1, 35.4, 51, 100),
            (35.5, 55.4, 101, 150),
            (55.5, 150.4, 151, 200),
            (150.5, 250.4, 201, 300),
            (250.5, 500.4, 301, 500)
        ],
        Pollutant.PM10: [
            (0, 54, 0, 50),
            (55, 154, 51, 100),
            (155, 254, 101, 150),
            (255, 354, 151, 200),
            (355, 424, 201, 300),
            (425, 604, 301, 500)
        ],
        Pollutant.O3: [  # 8-hour average
            (0.000, 0.054, 0, 50),
            (0.055, 0.070, 51, 100),
            (0.071, 0.085, 101, 150),
            (0.086, 0.105, 151, 200),
            (0.106, 0.200, 201, 300),
            (0.201, 0.604, 301, 500)  # Using 1-hour values for higher ranges
        ],
        Pollutant.NO2: [  # 1-hour average
            (0, 53, 0, 50),
            (54, 100, 51, 100),
            (101, 360, 101, 150),
            (361, 649, 151, 200),
            (650, 1249, 201, 300),
            (1250, 2049, 301, 500)
        ],
        Pollutant.SO2: [  # 1-hour average
            (0, 35, 0, 50),
            (36, 75, 51, 100),
            (76, 185, 101, 150),
            (186, 304, 151, 200),
            (305, 604, 201, 300),
            (605, 1004, 301, 500)
        ],
        Pollutant.CO: [  # 8-hour average in ppm
            (0.0, 4.4, 0, 50),
            (4.5, 9.4, 51, 100),
            (9.5, 12.4, 101, 150),
            (12.5, 15.4, 151, 200),
            (15.5, 30.4, 201, 300),
            (30.5, 50.4, 301, 500)
        ]
    }

    @staticmethod
    def calculate_individual_aqi(pollutant: Pollutant, concentration: float) -> int:
        """
        Calculate AQI for a single pollutant using EPA formula.
        
        Args:
            pollutant: The type of pollutant
            concentration: Concentration value in appropriate units
            
        Returns:
            AQI value (0-500)
        """
        if pollutant not in AQICalculator.EPA_BREAKPOINTS:
            raise ValueError(f"Unsupported pollutant: {pollutant}")
        
        breakpoints = AQICalculator.EPA_BREAKPOINTS[pollutant]
        
        # Find the appropriate breakpoint
        for c_low, c_high, i_low, i_high in breakpoints:
            if c_low <= concentration <= c_high:
                # EPA AQI formula: I = ((I_high - I_low) / (C_high - C_low)) * (C - C_low) + I_low
                aqi = ((i_high - i_low) / (c_high - c_low)) * (concentration - c_low) + i_low
                return round(aqi)
        
        # If concentration exceeds all breakpoints, return maximum AQI
        return 500

    @classmethod
    def calculate_aqi(cls, readings: List[PollutantReading]) -> Tuple[int, Pollutant]:
        """
        Calculate overall AQI from multiple pollutant readings.
        
        Args:
            readings: List of pollutant readings
            
        Returns:
            Tuple of (overall_aqi, dominant_pollutant)
        """
        if not readings:
            return 0, Pollutant.PM2_5
        
        aqi_values = {}
        
        for reading in readings:
            try:
                aqi = cls.calculate_individual_aqi(reading.pollutant, reading.concentration)
                aqi_values[reading.pollutant] = aqi
            except ValueError:
                # Skip unsupported pollutants
                continue
        
        if not aqi_values:
            return 0, Pollutant.PM2_5
        
        # Overall AQI is the maximum individual AQI
        max_aqi = max(aqi_values.values())
        dominant_pollutant = max(aqi_values, key=aqi_values.get)
        
        return max_aqi, dominant_pollutant

    @classmethod
    def create_air_quality_reading(
        cls,
        location: Location,
        pollutant_readings: List[PollutantReading],
        timestamp: Optional[datetime] = None,
        source: str = "System"
    ) -> AirQualityReading:
        """
        Create a complete air quality reading with calculated AQI.
        
        Args:
            location: Location of the measurement
            pollutant_readings: List of individual pollutant readings
            timestamp: When the reading was taken (defaults to now)
            source: Source of the data
            
        Returns:
            Complete AirQualityReading object
        """
        if timestamp is None:
            timestamp = datetime.now()
        
        aqi, dominant_pollutant = cls.calculate_aqi(pollutant_readings)
        
        return AirQualityReading(
            location=location,
            aqi=aqi,
            dominant_pollutant=dominant_pollutant,
            category=None,  # Will be set in __post_init__
            readings=pollutant_readings,
            timestamp=timestamp,
            source=source
        )