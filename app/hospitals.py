from .db import get_connection

def get_hospitals_in_bounds(min_lat, max_lat, min_lon, max_lon):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT name, ST_X(ST_Transform(way, 4326)), ST_Y(ST_Transform(way, 4326))
        FROM planet_osm_point 
        WHERE amenity = 'hospital'
          AND name IS NOT NULL
          AND ST_Y(ST_Transform(way, 4326)) BETWEEN %s AND %s
          AND ST_X(ST_Transform(way, 4326)) BETWEEN %s AND %s
        LIMIT 500;
    """, (min_lat, max_lat, min_lon, max_lon))
    
    results = cur.fetchall()
    cur.close()
    conn.close()

    return [{"name": r[0], "lon": r[1], "lat": r[2]} for r in results]
