import geopandas
import matplotlib.pyplot as plt

###############################################################################
# Let's use the NYC borough boundary data that is available in geopandas
# datasets. Plotting this gives the following result:

df = geopandas.read_file(geopandas.datasets.get_path('nybb'))
ax = df.plot(figsize=(10, 10), alpha=0.5, edgecolor='k')
plt.show()
geopandas.datasets.available()

###############################################################################
# Convert the data to Web Mercator
# ================================
#
# Web map tiles are typically provided in
# `Web Mercator <https://en.wikipedia.org/wiki/Web_Mercator>`__
# (`EPSG 3857 <https://epsg.io/3857>`__), so we need to make sure to convert
# our data first to the same CRS to combine our polygons and background tiles
# in the same map:

df = df.to_crs(epsg=3857)



###############################################################################

###############################################################################
# Add background tiles to plot
# ============================
#
# We can use `add_basemap` function of contextily to easily add a background
# map to our plot. :


###############################################################################
# We can control the detail of the map tiles using the optional `zoom` keyword
# (be careful to not specify a too high `zoom` level,
# as this can result in a large download).:


###############################################################################
# By default, contextily uses the Stamen Terrain style. We can specify a
# different style using ``ctx.providers``