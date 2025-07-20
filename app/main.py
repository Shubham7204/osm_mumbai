from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.hospitals import get_hospitals_in_bounds

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
def read_map(request: Request):
    return templates.TemplateResponse("map.html", {"request": request})

@app.get("/api/hospitals")
def hospitals(
    min_lat: float = Query(...),
    max_lat: float = Query(...),
    min_lon: float = Query(...),
    max_lon: float = Query(...)
):
    data = get_hospitals_in_bounds(min_lat, max_lat, min_lon, max_lon)
    return JSONResponse(content=data)