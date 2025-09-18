# 🌍 Global Air Quality Monitoring System

A comprehensive air quality monitoring system that uses Air Quality Index (AQI) by location to monitor air quality across different air categories worldwide.

## ✨ Features

- **Real-time Air Quality Monitoring**: Track AQI values for major cities worldwide
- **Multi-Pollutant Support**: Monitor PM2.5, PM10, O3, NO2, SO2, and CO levels
- **Interactive Dashboard**: Beautiful web interface with maps and charts
- **AQI Categories**: Color-coded air quality categories (Good, Moderate, Unhealthy, etc.)
- **REST API**: Programmatic access to air quality data
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Extensible Architecture**: Support for multiple data sources

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Hemara24/Global-Air-Quality-Monitoring-.git
   cd Global-Air-Quality-Monitoring-
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables** (optional):
   ```bash
   cp .env.example .env
   # Edit .env with your preferred settings
   ```

5. **Run the application**:
   ```bash
   python app.py
   ```

6. **Open your browser** and navigate to:
   ```
   http://localhost:5000
   ```

## 📊 Dashboard Features

### Overview Cards
- Real-time AQI values for monitored locations
- Color-coded categories for quick assessment
- Country and location information

### Interactive Map
- Global view of air quality data
- Click markers for detailed information
- Color-coded markers based on AQI levels

### Detailed Information Table
- Comprehensive data for all locations
- Sortable columns
- Timestamp information
- Dominant pollutant identification

### AQI Legend
- Visual guide to air quality categories
- Color coding explanation
- AQI value ranges

## 🔧 API Endpoints

### Get All Air Quality Data
```http
GET /api/air-quality/all
```

### Get Air Quality for Specific Location
```http
GET /api/air-quality/{location_name}
```

### Get Monitored Locations
```http
GET /api/locations
```

### Get AQI Categories
```http
GET /api/categories
```

### Health Check
```http
GET /api/health
```

## 📈 AQI Categories

| Category | AQI Range | Color | Health Implications |
|----------|-----------|-------|-------------------|
| Good | 0-50 | 🟢 Green | Air quality is satisfactory |
| Moderate | 51-100 | 🟡 Yellow | Acceptable for most people |
| Unhealthy for Sensitive Groups | 101-150 | 🟠 Orange | Sensitive individuals may experience problems |
| Unhealthy | 151-200 | 🔴 Red | Everyone may experience problems |
| Very Unhealthy | 201-300 | 🟣 Purple | Health warnings of emergency conditions |
| Hazardous | 301-500 | 🔴 Maroon | Emergency conditions |

## 🧪 Testing

Run the test suite:
```bash
python -m pytest tests/ -v
```

Run specific tests:
```bash
python -m pytest tests/test_aqi_calculator.py -v
```

## 🏗️ Architecture

### Core Components

- **Models** (`src/air_quality/core/models.py`): Data structures for locations, pollutants, and readings
- **AQI Calculator** (`src/air_quality/core/aqi_calculator.py`): EPA-standard AQI calculation engine
- **Data Collectors** (`src/air_quality/data/collectors.py`): Pluggable data source implementations
- **API Routes** (`src/air_quality/api/routes.py`): Flask web API endpoints
- **Dashboard** (`templates/dashboard.html`): Interactive web interface

### Project Structure
```
Global-Air-Quality-Monitoring-/
├── src/
│   └── air_quality/
│       ├── core/          # Core functionality
│       ├── data/          # Data collection
│       ├── api/           # Web API
│       └── visualization/ # Charts and graphs
├── templates/             # HTML templates
├── static/               # CSS, JS, images
├── tests/                # Test files
├── config.py             # Configuration
├── app.py               # Main application
└── requirements.txt     # Dependencies
```

## 🔌 Data Sources

### Simulated Data (Default)
- Generates realistic air quality data for testing
- No API keys required
- Perfect for development and demonstrations

### OpenWeatherMap API (Optional)
- Real-time air quality data
- Requires API key (free tier available)
- Set `OPENWEATHERMAP_API_KEY` in `.env` file

### Extensible Design
- Easy to add new data sources
- Implement the collector interface
- Register in `DataCollectorFactory`

## ⚙️ Configuration

Environment variables can be set in `.env` file:

```env
# Flask Application
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
FLASK_DEBUG=True

# Data Collection
DEFAULT_DATA_COLLECTOR=simulated
DATA_REFRESH_INTERVAL=300

# API Keys (Optional)
OPENWEATHERMAP_API_KEY=your-api-key-here
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and add tests
4. Run tests: `python -m pytest`
5. Commit your changes: `git commit -am 'Add feature'`
6. Push to the branch: `git push origin feature-name`
7. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🌟 Acknowledgments

- EPA Air Quality Index standards
- OpenWeatherMap for air quality data API
- Bootstrap for responsive UI components
- Leaflet for interactive maps
- Flask for the web framework

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/Hemara24/Global-Air-Quality-Monitoring-/issues) page
2. Create a new issue with detailed information
3. Include steps to reproduce the problem

---

**Made with ❤️ for cleaner air and better health**
