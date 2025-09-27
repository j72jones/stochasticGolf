import geopandas as gpd
# from pykml import parser
import numpy as np
import requests
# from osgeo import gdal
import pandas as pd

def parse_kml_to_geojson(kml_file_path):
    """Convert KML to GeoJSON with proper CRS"""
    # Read KML
    gdf = gpd.read_file(kml_file_path)
    
    # Ensure WGS84 (EPSG:4326)
    if gdf.crs is None:
        gdf = gdf.set_crs('EPSG:4326')
    elif gdf.crs != 'EPSG:4326':
        gdf = gdf.to_crs('EPSG:4326')
    
    return gdf


def get_usgs_elevation_points(geometry, resolution=1):
    """
    Get elevation points from USGS 3DEP for a geometry
    resolution: 1 (1m), 1/3 (1/3 arc-second), 1/9 (1/9 arc-second)
    """
    # Get bounding box
    bounds = geometry.bounds  # [minx, miny, maxx, maxy]
    
    # USGS Elevation Point Query Service
    url = "https://epqs.nationalmap.gov/v1/json"
    
    # Sample points within the geometry
    elevations = []
    if geometry.geom_type == 'Polygon':
        # Create grid of points within polygon
        x_coords = np.linspace(bounds[0], bounds[2], num=50)
        y_coords = np.linspace(bounds[1], bounds[3], num=50)
        
        i = 0

        for x in x_coords:
            for y in y_coords:
                i += 1
                point = f"{y},{x}"  # Note: lat,lon order
                params = {
                    'x': x, 'y': y, 
                    'units': 'Meters',
                    'output': 'json'
                }
                try:
                    response = requests.get(url, params=params, timeout=5)
                    if response.status_code == 200:
                        data = response.json()
                        elev = data.get('value')
                        if elev is not None:
                            elevations.append((x, y, elev))
                            print(i, x,y,elev)
                except:
                    continue
    
    return elevations


# Example usage
kml_gdf = parse_kml_to_geojson('Hole 12.kml')
print(f"Features found: {len(kml_gdf)}")
for idx, row in kml_gdf.iterrows():
    print("Check 1")
    print(f"{row.get('Name', f'Feature_{idx}')}: {row.geometry.geom_type}")
    print("Check 2")
    elev = get_usgs_elevation_points(row.geometry)
    df = pd.DataFrame(elev)
    df.to_csv(f"hole_12_data/{row.get('Name')}.csv", index=False)