from fastapi import FastAPI, HTTPException
import requests
from dotenv import load_dotenv
import os

app = FastAPI()
load_dotenv()

TOMTOM_API_KEY = os.getenv("TOMTOM_API_KEY")
print(TOMTOM_API_KEY)

@app.get("/distance/")
async def get_distance(zipcode1: str, zipcode2: str):
    # Step 1: Geocode the first zip code
    coord1 = geocode_zipcode(zipcode1)
    if not coord1:
        raise HTTPException(status_code=400, detail="Invalid first zip code")

    # Step 2: Geocode the second zip code
    coord2 = geocode_zipcode(zipcode2)
    if not coord2:
        raise HTTPException(status_code=400, detail="Invalid second zip code")

    # Step 3: Calculate the route distance
    distance = calculate_route(coord1, coord2)
    if distance is None:
        raise HTTPException(status_code=400, detail="Could not calculate route distance")

    return {"distance_mi": distance / 1609}  # Return distance in kilometers

def geocode_zipcode(zipcode: str):
    url = f"https://api.tomtom.com/search/2/geocode/{zipcode}.json?countrySet=US&key={TOMTOM_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data["results"]:
            position = data["results"][0]["position"]
            return position["lat"], position["lon"]
    return None

def calculate_route(coord1, coord2):
    url = (
        f"https://api.tomtom.com/routing/1/calculateRoute/"
        f"{coord1[0]},{coord1[1]}:{coord2[0]},{coord2[1]}/json"
        f"?routeType=fastest&traffic=false&travelMode=car&key={TOMTOM_API_KEY}"
    )
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data.get("routes"):
            return data["routes"][0]["summary"]["lengthInMeters"]
    return None
