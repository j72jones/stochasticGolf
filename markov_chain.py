import geopandas as gpd
import numpy as np
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


data_points = pd.read_csv("hole_12_data/full_square.csv")
print(data_points.tail())
diffs = np.diff(np.sort(data_points["0"].to_numpy()))
x_gap = diffs[diffs > 0].min()
diffs = np.diff(np.sort(data_points["1"].to_numpy()))
y_gap = diffs[diffs > 0].min()




# df has columns: lon, lat, altitude
gdf_points = gpd.GeoDataFrame(data_points, geometry=gpd.points_from_xy(data_points["0"], data_points["1"]), crs="EPSG:4326")

# reproject to meters (example: UTM zone 16N)
gdf_points = gdf_points.to_crs("EPSG:32616")

# make rectangles
from shapely.geometry import box
def make_rectangle(x, y, width, height):
    half_w = width / 2.0
    half_h = height / 2.0
    return box(x - half_w, y - half_h, x + half_w, y + half_h)
gdf_points["geometry"] = gdf_points.geometry.apply(lambda p: make_rectangle(p.x, p.y, x_gap, y_gap))


def area_fraction(square, geom):
    inter = square.intersection(geom)
    if inter.is_empty:
        return 0.0
    return inter.area / square.area


kml_gdf = parse_kml_to_geojson('hole_12_data/Hole 12 playable.kml')
kml_gdf = kml_gdf.to_crs("EPSG:32616")

print(f"Features found: {len(kml_gdf)}")
for idx, row in kml_gdf.iterrows():
    print(f"{row.get('Name', f'Feature_{idx}')}: {row.geometry.geom_type}")
    gdf_points[f"frac {row.get('Name')}"] = gdf_points.geometry.apply(lambda sq: area_fraction(sq, row.geometry))

print("gdf bounds", gdf_points.total_bounds)   # bounding box of your grid (meters)
print("kml bounds", kml_gdf.total_bounds)      # bounding box of KML polygons (meters, after to_crs)


print(gdf_points[gdf_points["frac Green"] > 0])

gdf_points = gdf_points.rename(columns={"0": 'lon', "1": 'lat', "2": 'alt', "frac Green": "Green"})

gdf_points["Fairway"] = gdf_points["frac Fairway 1"] + gdf_points["frac Fairway 2"] - gdf_points["Green"]

import numpy as np

# rough conversion: 1 degree latitude ≈ 111 km
deg_to_m = 111_000  

# get min values
min_lon = gdf_points['lon'].min()
min_lat = gdf_points['lat'].min()
mean_lat = gdf_points['lat'].mean()

# convert to meters relative to minimum
gdf_points['x'] = (gdf_points['lon'] - min_lon) * deg_to_m * np.cos(np.radians(mean_lat))  # east-west distance
gdf_points['y'] = (gdf_points['lat'] - min_lat) * deg_to_m                                # north-south distance

import math
gdf_points["club"] = "9 Iron"
gdf_points["dist"] = np.random.uniform(60,300, size = len(gdf_points))
gdf_points["angle"] = np.random.uniform(0,2 * math.pi, size = len(gdf_points))
gdf_points["mean"] = np.random.uniform(1,6, size=len(gdf_points))

gdf_points = gdf_points[["lon", "lat", "alt", "x", "y", "Fairway", "Green", "club", "dist", "angle", "mean"]]
# print(gdf_points[["lon", "lat", "alt", "Fairway", "Green"]].max())
gdf_points = gdf_points[gdf_points["Fairway"] + gdf_points["Green"] > 0]

print(gdf_points[["lon", "lat", "alt", "Fairway", "Green"]].max())

gdf_points.to_csv("hole_12_data/hole_12_temp_data.csv")