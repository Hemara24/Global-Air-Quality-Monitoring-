"""
Core data models for air quality monitoring system.
"""
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional, Dict, List


class AQICategory(Enum):
    """Air Quality Index categories based on EPA standards."""
    GOOD = ("Good", 0, 50, "#00E400")
    MODERATE = ("Moderate", 51, 100, "#FFFF00")
    UNHEALTHY_SENSITIVE = ("Unhealthy for Sensitive Groups", 101, 150, "#FF7E00")
    UNHEALTHY = ("Unhealthy", 151, 200, "#FF0000")
    VERY_UNHEALTHY = ("Very Unhealthy", 201, 300, "#8F3F97")
    HAZARDOUS = ("Hazardous", 301, 500, "#7E0023")

    def __init__(self, label: str, min_aqi: int, max_aqi: int, color: str):
        self.label = label
        self.min_aqi = min_aqi
        self.max_aqi = max_aqi
        self.color = color

    @classmethod
    def from_aqi(cls, aqi_value: int) -> 'AQICategory':
        """Get category from AQI value."""
        for category in cls:
            if category.min_aqi <= aqi_value <= category.max_aqi:
                return category
        return cls.HAZARDOUS  # Default for values > 500


class Pollutant(Enum):
    """Supported air pollutants."""
    PM2_5 = "PM2.5"
    PM10 = "PM10"
    O3 = "O3"
    NO2 = "NO2"
    SO2 = "SO2"
    CO = "CO"


@dataclass
class Location:
    """Represents a geographical location."""
    name: str
    latitude: float
    longitude: float
    country: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None


@dataclass
class PollutantReading:
    """Individual pollutant measurement."""
    pollutant: Pollutant
    concentration: float  # in appropriate units (μg/m³, ppm, etc.)
    unit: str
    timestamp: datetime


@dataclass
class AirQualityReading:
    """Complete air quality reading for a location."""
    location: Location
    aqi: int
    dominant_pollutant: Pollutant
    category: AQICategory
    readings: List[PollutantReading]
    timestamp: datetime
    source: str = "Unknown"

    def __post_init__(self):
        """Set category based on AQI value."""
        self.category = AQICategory.from_aqi(self.aqi)


@dataclass
class AirQualityAlert:
    """Alert for poor air quality conditions."""
    location: Location
    aqi: int
    category: AQICategory
    message: str
    timestamp: datetime
    active: bool = True