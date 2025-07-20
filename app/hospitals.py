from .db import get_connection

def get_hospitals_in_bounds(min_lat, max_lat, min_lon, max_lon):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT name, lon, lat
        FROM hospitals
        WHERE lat BETWEEN %s AND %s
          AND lon BETWEEN %s AND %s
          AND name IS NOT NULL
        LIMIT 500;
    """, (min_lat, max_lat, min_lon, max_lon))
    
    results = cur.fetchall()
    cur.close()
    conn.close()

    return [{"name": r[0], "lon": r[1], "lat": r[2]} for r in results]