import requests
import time

TOKEN = "5d884a451880e821b8e4c7ed3a8727ce0eb30650"

_cached_data = None
_last_fetch_time = 0


def fetch_live_aqi():
    url = f"https://api.waqi.info/map/bounds/?latlng=28.3,76.8,28.9,77.5&token={TOKEN}"
    
    response = requests.get(url)
    data = response.json()

    stations = []

    if data["status"] == "ok":
        for station in data["data"]:
            stations.append({
                "name": station["station"]["name"],
                "lat": station["lat"],
                "lon": station["lon"],
                "aqi": int(station["aqi"]) if station["aqi"] != "-" else 0
            })

    return stations


def fetch_live_aqi_cached():
    global _cached_data, _last_fetch_time

    current_time = time.time()

    # refresh every 5 minutes
    if current_time - _last_fetch_time > 300 or _cached_data is None:
        print("Fetching fresh AQI data (single API call)...")
        _cached_data = fetch_live_aqi()
        _last_fetch_time = current_time

    return _cached_data