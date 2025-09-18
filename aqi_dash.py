import pandas as pd
import numpy as np
from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource, HoverTool, LinearColorMapper, ColorBar, Select, Slider
from bokeh.layouts import column, row
from bokeh.palettes import Plasma256
from bokeh.models import WMTSTileSource
from pyproj import Transformer
from bokeh.models import CustomJS

print("Loading air quality data...")

# Load the dataset
try:
    df = pd.read_csv('CAQI.csv')
    print("Dataset loaded successfully.")
except FileNotFoundError:
    print("ERROR: CAQI.csv not found. Please ensure the file exists.")
    exit()

# Clean and prepare data
df = df.dropna(subset=['lat', 'lng', 'AQI Value'])
df = df.rename(columns={'lng': 'lon'})
df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
df = df.dropna(subset=['timestamp'])

# Create risk categories
def categorize_aqi(aqi):
    if aqi <= 50: return "Good"
    elif aqi <= 100: return "Moderate"
    elif aqi <= 150: return "Unhealthy"
    else: return "Hazardous"

df['risk'] = df['AQI Value'].apply(categorize_aqi)

# Convert coordinates
def wgs84_to_web_mercator(lon, lat):
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True)
    x, y = transformer.transform(lon, lat)
    return x, y

df['x'], df['y'] = wgs84_to_web_mercator(df['lon'].values, df['lat'].values)

# Prepare time data
df['time_numeric'] = (df['timestamp'] - df['timestamp'].min()).dt.total_seconds()
time_min = int(df['time_numeric'].min())
time_max = int(df['time_numeric'].max())

# Create data source
source = ColumnDataSource(data=df)

# Set up the plot
p = figure(
    x_axis_type="mercator",
    y_axis_type="mercator",
    tools="pan,wheel_zoom,box_zoom,reset,save",
    title="Global Air Quality Monitoring Dashboard",
    width=1000,
    height=600
)
p.add_tile(WMTSTileSource(url='https://tiles.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png'))

# Task 4: Choropleth-style visualization
choropleth_mapper = LinearColorMapper(
    palette=Plasma256,
    low=df['AQI Value'].min(),
    high=df['AQI Value'].max(),
    nan_color='gray'
)

points = p.circle(
    x='x',
    y='y',
    source=source,
    size=12,
    color={'field': 'AQI Value', 'transform': choropleth_mapper},
    alpha=0.8,
    line_color='white',
    line_width=0.5,
    legend_label="AQI Intensity"
)

color_bar = ColorBar(
    color_mapper=choropleth_mapper,
    label_standoff=15,
    width=20,
    height=400,
    location=(0, 0),
    title="AQI Value",
    title_text_font_size='12pt'
)
p.add_layout(color_bar, 'right')

# Hover tooltips
hover = HoverTool(
    renderers=[points],
    tooltips=[
        ("City", "@City"),
        ("Country", "@Country"),
        ("AQI Value", "@{AQI Value}"),
        ("AQI Category", "@{AQI Category}"),
        ("PM2.5", "@{PM2.5 AQI Value}"),
        ("Ozone", "@{Ozone AQI Value}"),
        ("Timestamp", "@timestamp{%F %T}"),
        ("(Location)", "(@lat, @lon)")
    ],
    formatters={'@timestamp': 'datetime'}
)
p.add_tools(hover)

# Time slider
time_slider = Slider(start=time_min, end=time_max, value=time_min, 
                    step=3600, title="Time (seconds from start)")

time_slider.js_on_change('value', CustomJS(args={'source': source}, code="""
    const data = source.data;
    const selected_time = cb_obj.value;
    const time_data = data['time_numeric'];
    const n = time_data.length;
    
    const new_indices = [];
    for (let i = 0; i < n; i++) {
        if (Math.abs(time_data[i] - selected_time) < 1800) {
            new_indices.push(i);
        }
    }
    source.selected.indices = new_indices;
"""))

# Category filter
risk_options = ['All'] + sorted(df['risk'].unique().tolist())
risk_filter = Select(title="Filter by Risk Level:", value="All", options=risk_options)

risk_filter.js_on_change('value', CustomJS(args={'source': source}, code="""
    const selected_risk = cb_obj.value;
    const risk_data = source.data['risk'];
    const n = risk_data.length;
    
    const new_indices = [];
    for (let i = 0; i < n; i++) {
        if (selected_risk === 'All' || risk_data[i] === selected_risk) {
            new_indices.push(i);
        }
    }
    source.selected.indices = new_indices;
"""))

# Final layout
layout = column(risk_filter, time_slider, p)
curdoc().add_root(layout)
curdoc().title = "Global Air Quality Dashboard"

print("Air Quality Dashboard started successfully!")
print("Access at: http://localhost:5006/aqi_dashboard")