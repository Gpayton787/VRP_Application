import pandas as pd
import matplotlib.pyplot as plt
import descartes
import geopandas as gpd
from shapely.geometry import Point, Polygon

# street_map = gpd.read_file('./assets/layers/POLYGON.shp')
fig, ax = plt.subplots(figsize=(15,15))
# street_map.plot(ax=ax)

# Load the shapefile
shapefile_path = './assets/layers/POLYGON.shp'
gdf = gpd.read_file(shapefile_path)
gdf2 = gpd.read_file('./assets/layers/POINT.shp')
# Plot the shapefile
gdf.plot()
gdf2.plot()
plt.show()

