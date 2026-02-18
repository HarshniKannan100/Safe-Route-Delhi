from fastapi import FastAPI
from route_scorer import find_safest_route
from aqi_service import fetch_live_aqi_cached
from geocoding import geocode_place
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow all origins for hackathon
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/safe-route")
def safe_route(source: str, destination: str):

    # Convert names → lat/lon
    source_coords = geocode_place(source)
    dest_coords = geocode_place(destination)

    if not source_coords or not dest_coords:
        return {"error": "Invalid location name"}

    stations = fetch_live_aqi_cached()

    result = find_safest_route(
        source_coords[0], source_coords[1],
        dest_coords[0], dest_coords[1],
        stations
    )

    return {
        "source": source,
        "destination": destination,
        "result": result
    }