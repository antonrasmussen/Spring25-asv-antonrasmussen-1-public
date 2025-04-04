# !pip install geopandas
# !pip install pysal
# !pip install mapclassify

import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import os
os.environ["SHAPE_RESTORE_SHX"] = "YES"

urban_areas = gpd.read_file("content/tl_2024_us_uac20.shp")

print(urban_areas.columns)

df_dummy_data = pd.DataFrame({
    "UACE20": urban_areas["UACE20"],
    "VALUE": np.random.randint(100, 10000, size=len(urban_areas))
})

urban_merged = urban_areas.merge(df_dummy_data, on="UACE20")
urban_merged = urban_merged.to_crs(epsg=5070)  # Reproject to Albers (NAD83 / Conus Albers)
# Filter the data to only include the contiguous US
#    The EPSG:5070 projection is used for the contiguous US.
#    The coordinates are in meters, so we can use the following bounding box:
#    -2.3e6 to 2.6e6 for x-coordinates (longitude)
#    1.0e5 to 3.2e6 for y-coordinates (latitude)
#    This will filter the data to only include the contiguous US.

urban_merged_conus = urban_merged.cx[-2.3e6:2.6e6, 1.0e5:3.2e6]

fig, ax = plt.subplots(figsize=(16, 12))
urban_merged_conus.plot(
    column="VALUE",
    cmap="Blues",
    scheme="Quantiles",
    k=5,
    edgecolor="black",
    linewidth=0.3,
    legend=True,
    ax=ax
)
ax.set_title("Urban Areas in Contiguous US", fontsize=14)
ax.axis("off")
plt.show()
