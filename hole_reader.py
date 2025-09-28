import numpy as np
import pandas as pd
import requests


def get_usgs_elevation_points(lon_1, lat_1, lon_2, lat_2, resolution=1):
    """
    Get elevation points from USGS 3DEP for a geometry
    resolution: 1 (1m), 1/3 (1/3 arc-second), 1/9 (1/9 arc-second)
    """
    # Get bounding box
    # bounds = geometry.bounds  # [minx, miny, maxx, maxy]
    
    # USGS Elevation Point Query Service
    url = "https://epqs.nationalmap.gov/v1/json"
    
    # Sample points within the geometry
    elevations = []
    # if geometry.geom_type == 'Polygon':
    # Create grid of points within polygon
    x_coords = np.linspace(lat_1, lat_2, num=50)
    y_coords = np.linspace(lon_1, lon_2, num=50)
    
    i = 0

    for x in x_coords:
        for y in y_coords:
            i += 1
            params = {
                'x': x, 'y': y, 
                'units': 'Meters',
                'output': 'json'
            }
            try:
                response = requests.get(url, params=params, timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    elev = data.get("value")
                    if elev is not None:
                        elevations.append((x, y, elev))
                        print(i, x,y,elev)
            except Exception as e:
                print(i, e)
                continue
    
    return elevations

print("Starting")
elev = get_usgs_elevation_points(34+4/60+49/3600,  -(84+13/60+40/3600), 34+4/60+46/3600, -(84+13/60+24/6000))
df = pd.DataFrame(elev)
df.to_csv(f"hole_12_data/full_square.csv", index=False)