import requests
import datetime

WEATHER_CODES = {
    0: "Sunny",
    1: "Mainly Sunny",
    2: "Partly Cloudy",
    3: "Cloudy",
    45: "Foggy",
    48: "Rime Fog",
    51: "Light Drizzle",
    53: "Drizzle",
    55: "Heavy Drizzle",
    56: "Light Freezing Drizzle",
    57: "Freezing Drizzle",
    61: "Light Rain",
    63: "Rain",
    65: "Heavy Rain",
    66: "Light Freezing Rain",
    67: "Freezing Rain",
    71: "Light Snow",
    73: "Snow",
    75: "Heavy Snow",
    77: "Snow Grains",
    80: "Light Showers",
    81: "Showers",
    82: "Heavy Showers",
    85: "Light Snow Showers",
    86: "Snow Showers",
    95: "Thunderstorm",
    96: "Light Thunderstorms With Hail",
    99: "Thunderstorm With Hail"
}

WIND_ARROWS = ['↑ N', '↗ NE', '→ E', '↘ SE', '↓ S', '↙ SW', '← W', '↖ NW']

def get_wind_dir(deg):
    idx = int((deg + 22.5) % 360 / 45)
    return WIND_ARROWS[idx]

def fetch_weather(lat, lon, config):
    temp_unit   = "celsius" if config["units_temp"]   == "°C" else "fahrenheit"
    precip_unit = "mm"      if config["units_precip"] == "mm" else "inch"
    
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,precipitation,wind_speed_10m,wind_direction_10m,weather_code",
        "hourly": "temperature_2m,precipitation,weather_code",
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,weather_code",
        "temperature_unit": temp_unit,
        "precipitation_unit": precip_unit,
        "timezone": "auto",
    }
    response = requests.get(url, params = params)
    if response.status_code == 200:
        return response.json()
    return None