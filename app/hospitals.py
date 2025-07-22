import os
import random
import psycopg2
from dotenv import load_dotenv

load_dotenv()

# This function to connect to the database stays the same
def get_connection():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT"))
    )

# NEW FUNCTION 1: Find "POIs" using your hospitals table
# This does NOT require PostGIS or changing your table. It calculates distance in the query.
def find_pois_in_radius_from_hospitals(lat: float, lon: float, radius_km: float):
    """
    Searches the hospitals table within a certain radius.
    It pretends hospitals are POIs for the demo.
    """
    conn = get_connection()
    cur = conn.cursor()
    
    # This SQL query calculates the distance to find hospitals within the radius.
    cur.execute("""
        SELECT name, lat, lon FROM (
            SELECT *, ( 6371 * acos( cos( radians(%s) ) * cos( radians( lat ) ) * cos( radians( lon ) - radians(%s) ) + sin( radians(%s) ) * sin( radians( lat ) ) ) ) AS distance
            FROM hospitals
        ) AS subquery
        WHERE distance < %s AND lat IS NOT NULL AND lon IS NOT NULL
        ORDER BY distance
        LIMIT 100;
    """, (lat, lon, lat, radius_km))
    
    results = cur.fetchall()
    cur.close()
    conn.close()

    pois = []
    for r in results:
        # For the demo, randomly flag some POIs as "predictive"
        is_predictive = random.random() < 0.1 # 10% chance of being flagged
        pois.append({
            "name": r[0], 
            "lat": r[1], 
            "lon": r[2],
            "is_predictive": is_predictive
        })
    return pois

# NEW FUNCTION 2: Generate FAKE crime data for the heatmap
def generate_fake_crime_hotspots():
    """
    This function creates fake crime data.
    It gets a few real hospital locations and adds random points around them.
    This gives you a realistic heatmap for the demo without needing a real crime table.
    """
    conn = get_connection()
    cur = conn.cursor()
    # Get 50 random hospitals to act as the center of crime clusters
    cur.execute("SELECT lat, lon FROM hospitals WHERE lat IS NOT NULL AND lon IS NOT NULL ORDER BY RANDOM() LIMIT 50;")
    hospital_centers = cur.fetchall()
    cur.close()
    conn.close()

    crime_points = []
    for (h_lat, h_lon) in hospital_centers:
        # For each hospital, generate 10 to 30 fake crime incidents nearby
        for _ in range(random.randint(10, 30)):
            offset_lat = random.uniform(-0.005, 0.005)
            offset_lon = random.uniform(-0.005, 0.005)
            crime_lat = h_lat + offset_lat
            crime_lon = h_lon + offset_lon
            intensity = random.uniform(0.5, 1.0) # Intensity for the heatmap
            crime_points.append([crime_lat, crime_lon, intensity]) # Format for Leaflet.heat
            
    return crime_points