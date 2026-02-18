import requests

def geocode_place(place_name):
    url = "https://nominatim.openstreetmap.org/search"
    
    params = {
        "q": place_name,
        "format": "json",
        "limit": 1
    }

    response = requests.get(url, params=params, headers={"User-Agent": "aqi-app"})
    data = response.json()

    if len(data) == 0:
        return None

    return float(data[0]["lat"]), float(data[0]["lon"])