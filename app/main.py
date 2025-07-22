from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

# Import our NEW functions from the other file
from app.hospitals import find_pois_in_radius_from_hospitals, generate_fake_crime_hotspots

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

# This serves your main HTML page
@app.get("/", response_class=HTMLResponse)
def read_map(request: Request):
    return templates.TemplateResponse("map.html", {"request": request})

# NEW API ENDPOINT 1: For finding POIs
@app.get("/api/pois-in-radius")
def pois_in_radius(lat: float, lon: float, radius_km: float):
    # This calls the function that searches your hospitals table
    data = find_pois_in_radius_from_hospitals(lat, lon, radius_km)
    return JSONResponse(content=data)

# NEW API ENDPOINT 2: For the crime heatmap
@app.get("/api/crime-hotspots")
def crime_hotspots():
    # This calls the function that generates FAKE crime data
    data = generate_fake_crime_hotspots()
    return JSONResponse(content=data)