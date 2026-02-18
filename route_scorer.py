from utils import haversine
import requests


# -----------------------------
# 1️⃣ Find nearest AQI station
# -----------------------------
def get_nearest_aqi(lat, lon, stations):
    min_dist = float("inf")
    nearest_aqi = None

    for station in stations:
        dist = haversine(lat, lon, station["lat"], station["lon"])

        if dist < min_dist:
            min_dist = dist
            nearest_aqi = station["aqi"]

    return nearest_aqi


# -----------------------------
# 2️⃣ Calculate route score
# -----------------------------
def calculate_route_score(route_points, stations):
    total_aqi = 0

    for lat, lon in route_points:
        aqi = get_nearest_aqi(lat, lon, stations)

        if aqi is not None:
            total_aqi += aqi

    return total_aqi / len(route_points)

def get_route_checkpoints(route_points, stations):
    visited_places = set()

    for lat, lon in route_points:
        for station in stations:
            dist = haversine(lat, lon, station["lat"], station["lon"])

            # If route passes within ~1.5 km of station
            if dist < 1.5:
                visited_places.add(station["name"])

    return list(visited_places)
# -----------------------------
# 3️⃣ Get routes from OSRM
# -----------------------------
def get_routes_osrm(source_lat, source_lon, dest_lat, dest_lon):
    url = (
        f"http://router.project-osrm.org/route/v1/driving/"
        f"{source_lon},{source_lat};{dest_lon},{dest_lat}"
        f"?alternatives=true&geometries=geojson"
    )

    response = requests.get(url)
    data = response.json()

    routes = []

    for route in data["routes"]:
        coords = route["geometry"]["coordinates"]

        # Convert (lon, lat) → (lat, lon)
        route_points = [(lat, lon) for lon, lat in coords]

        routes.append(route_points)

    return routes


# -----------------------------
# 4️⃣ Main function
# -----------------------------
def find_safest_route(source_lat, source_lon, dest_lat, dest_lon, stations):

    routes = get_routes_osrm(source_lat, source_lon, dest_lat, dest_lon)

    scores = []
    route_places = []

    for route in routes:
        sampled_points = route[::10] if len(route) > 25 else route

        score = calculate_route_score(sampled_points, stations)
        scores.append(score)

        places = get_route_checkpoints(sampled_points, stations)
        route_places.append(places)

    best_index = scores.index(min(scores))

    best_score = min(scores)
    worst_score = max(scores)

    reduction_percent = round(
        ((worst_score - best_score) / worst_score) * 100, 2
    )

    return {
        "routes": routes,
        "scores": scores,
        "route_places": route_places,
        "best_route_index": best_index,
        "pollution_reduction_percent": reduction_percent
    }