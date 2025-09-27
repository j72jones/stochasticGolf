import pandas as pd

data = pd.read_csv("hole_12_data/Fairway 1.csv")

lon = data["0"]
lat = data["1"]
alt = data["2"]

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata

# Your data
# lon, lat, alt = arrays of raw points
points = np.column_stack((lon, lat))
values = alt

# Define a regular grid
grid_lon = np.linspace(lon.min(), lon.max(), 50)
grid_lat = np.linspace(lat.min(), lat.max(), 50)
grid_X, grid_Y = np.meshgrid(grid_lon, grid_lat)

# Interpolate alt values onto grid
grid_Z = griddata(points, values, (grid_X, grid_Y), method="cubic")

# Plot contour
plt.figure(figsize=(8,6))
plt.contourf(grid_lon, grid_lat, grid_Z, cmap="terrain")
plt.colorbar(label="Elevation (m)")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title("Interpolated Terrain Map")
plt.show()



def simulate_shot(x,y,club,theta, count):
    pass
    return [(0,0) for _ in range(count)]


"""
Data in form
X_1|X_2|Y_1|Y_2|Z|fairway|drop
...

With 2 extra points

start = (x,y)
hole = (x,y)
and a green polygon

Green polygon, we apply a log(d+1)+1 scale where d is the distance from the hole for "how difficult"

Filter data for only state that have some fairway
Markov chain has 2 states for each fairway state (1 standard state and 1 feeder state for drops)
Need to decide how to deal with the green (absorbing state)
"""


def optimize_chain(state_info):
    pass