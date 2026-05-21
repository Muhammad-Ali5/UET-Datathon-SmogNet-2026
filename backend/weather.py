import requests
from pathlib import Path

try:
    from .config import OPENWEATHER_API_KEY
except ImportError:
    from config import OPENWEATHER_API_KEY

# Same coordinate mapping as used in process_datasets
CITY_COORDS = {
    "Lahore": {"lat": 31.5204, "lon": 74.3587},
    "Karachi": {"lat": 24.8607, "lon": 67.0011},
    "Islamabad": {"lat": 33.6844, "lon": 73.0479},
    "Peshawar": {"lat": 34.0151, "lon": 71.5249},
    "Quetta": {"lat": 30.1798, "lon": 66.9750}
}

def fetch_weather(city_name: str):
    """Return current weather data from OpenWeatherMap for a given city.
    Returns a dict with temperature (C), humidity, description, etc., or None on error.
    """
    coords = CITY_COORDS.get(city_name)
    if not coords or not OPENWEATHER_API_KEY:
        print(f"[Weather] Missing coordinates or API key for {city_name}")
        return None
    url = (
        f"http://api.openweathermap.org/data/2.5/weather?lat={coords['lat']}&lon={coords['lon']}"
        f"&appid={OPENWEATHER_API_KEY}&units=metric"
    )
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        main = data.get('main', {})
        weather_desc = data.get('weather', [{}])[0].get('description', '')
        return {
            "city": city_name,
            "temperature": main.get('temp'),
            "humidity": main.get('humidity'),
            "description": weather_desc,
            "source": "OpenWeatherMap"
        }
    except Exception as e:
        print(f"[Weather] Error fetching data for {city_name}: {e}")
        return None


def get_current_weather(city_name: str):
    """Wrapper for fetch_weather returning same dict or raising exception on failure."""
    data = fetch_weather(city_name)
    if data is None:
        raise RuntimeError(f"Weather data not available for {city_name}")
    return data
