"""
Data collectors for fetching air quality information from various sources.
"""

import requests
from datetime import datetime
from typing import Optional, Dict, Any
from ..core.models import Location, PollutantReading, Pollutant, AirQualityReading
from ..core.aqi_calculator import AQICalculator


class OpenWeatherMapCollector:
    """Collector for OpenWeatherMap Air Pollution API."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5/air_pollution"

    def fetch_current_data(self, location: Location) -> Optional[AirQualityReading]:
        """
        Fetch current air quality data for a location.

        Args:
            location: Location to fetch data for

        Returns:
            AirQualityReading or None if fetch fails
        """
        try:
            params = {
                "lat": location.latitude,
                "lon": location.longitude,
                "appid": self.api_key,
            }

            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()
            return self._parse_response(data, location)

        except Exception as e:
            print(f"Error fetching data from OpenWeatherMap: {e}")
            return None

    def _parse_response(
        self, data: Dict[Any, Any], location: Location
    ) -> AirQualityReading:
        """Parse OpenWeatherMap API response."""
        components = data["list"][0]["components"]
        timestamp = datetime.fromtimestamp(data["list"][0]["dt"])

        readings = []

        # Map OpenWeatherMap components to our pollutants
        pollutant_mapping = {
            "pm2_5": (Pollutant.PM2_5, "μg/m³"),
            "pm10": (Pollutant.PM10, "μg/m³"),
            "o3": (Pollutant.O3, "μg/m³"),
            "no2": (Pollutant.NO2, "μg/m³"),
            "so2": (Pollutant.SO2, "μg/m³"),
            "co": (Pollutant.CO, "mg/m³"),
        }

        for component, (pollutant, unit) in pollutant_mapping.items():
            if component in components:
                concentration = components[component]

                # Convert units if necessary for AQI calculation
                if pollutant == Pollutant.O3:
                    # Convert μg/m³ to ppm for ozone
                    concentration = concentration * 0.0005  # Approximate conversion
                elif pollutant == Pollutant.CO:
                    # Convert mg/m³ to ppm for CO
                    concentration = concentration * 0.873  # Approximate conversion

                readings.append(
                    PollutantReading(
                        pollutant=pollutant,
                        concentration=concentration,
                        unit=unit,
                        timestamp=timestamp,
                    )
                )

        return AQICalculator.create_air_quality_reading(
            location=location,
            pollutant_readings=readings,
            timestamp=timestamp,
            source="OpenWeatherMap",
        )


class SimulatedDataCollector:
    """Simulated data collector for testing and demonstration purposes."""

    def __init__(self):
        self.locations_data = {
            "New York": {"base_aqi": 75, "variation": 20},
            "Los Angeles": {"base_aqi": 95, "variation": 25},
            "Beijing": {"base_aqi": 155, "variation": 40},
            "London": {"base_aqi": 65, "variation": 15},
            "Delhi": {"base_aqi": 180, "variation": 50},
            "Tokyo": {"base_aqi": 55, "variation": 15},
        }

    def fetch_current_data(self, location: Location) -> AirQualityReading:
        """
        Generate simulated air quality data for a location.

        Args:
            location: Location to generate data for

        Returns:
            Simulated AirQualityReading
        """
        import random

        # Get base data or use defaults
        base_data = self.locations_data.get(
            location.name, {"base_aqi": 75, "variation": 20}
        )
        base_aqi = base_data["base_aqi"]
        variation = base_data["variation"]

        # Generate realistic pollutant readings
        readings = []
        timestamp = datetime.now()

        # PM2.5 (usually the dominant pollutant)
        pm25_concentration = max(
            0, random.normalvariate(base_aqi * 0.4, variation * 0.2)
        )
        readings.append(
            PollutantReading(
                pollutant=Pollutant.PM2_5,
                concentration=pm25_concentration,
                unit="μg/m³",
                timestamp=timestamp,
            )
        )

        # PM10
        pm10_concentration = max(0, pm25_concentration * random.uniform(1.2, 2.0))
        readings.append(
            PollutantReading(
                pollutant=Pollutant.PM10,
                concentration=pm10_concentration,
                unit="μg/m³",
                timestamp=timestamp,
            )
        )

        # O3
        o3_concentration = max(0, random.normalvariate(0.05, 0.02))
        readings.append(
            PollutantReading(
                pollutant=Pollutant.O3,
                concentration=o3_concentration,
                unit="ppm",
                timestamp=timestamp,
            )
        )

        # NO2
        no2_concentration = max(0, random.normalvariate(40, 15))
        readings.append(
            PollutantReading(
                pollutant=Pollutant.NO2,
                concentration=no2_concentration,
                unit="μg/m³",
                timestamp=timestamp,
            )
        )

        return AQICalculator.create_air_quality_reading(
            location=location,
            pollutant_readings=readings,
            timestamp=timestamp,
            source="Simulated Data",
        )


class DataCollectorFactory:
    """Factory for creating appropriate data collectors."""

    @staticmethod
    def create_collector(collector_type: str, **kwargs):
        """Create a data collector of specified type."""
        if collector_type.lower() == "openweathermap":
            api_key = kwargs.get("api_key")
            if not api_key:
                raise ValueError(
                    "OpenWeatherMap collector requires 'api_key' parameter"
                )
            return OpenWeatherMapCollector(api_key)
        elif collector_type.lower() == "simulated":
            return SimulatedDataCollector()
        else:
            raise ValueError(f"Unknown collector type: {collector_type}")
