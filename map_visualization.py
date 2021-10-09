"""
Developed by Aindriya Barua in October, 2021
Thoughrough explantion of the code can be found in on my medium blog: 
https://medium.com/@barua.aindriya/visualize-data-on-a-choropleth-map-with-geopandas-and-matplotlib-924cedd8e9cb
"""

# required imports

import xlrd
import random
import pandas as pd
import seaborn as sns
import geopandas as gpd
import matplotlib.pyplot as plt

import matplotlib.colors as colors
import numpy as np

sns.set_style('whitegrid')

# Read the first sheet from the Excel File

file_name = 'statewise-eng.csv'
csv_df = pd.read_csv(file_name)
columns = csv_df.columns

states_csv = csv_df[columns[0]].tolist()
know_english_csv = csv_df[columns[1]].tolist()

# reading the state wise shapefile of India in a GeoDataFrame and preview it

fp = "Igismap/Indian_States.shp"
map_df = gpd.read_file(fp)
states_and_ut = map_df['st_nm'].tolist()
print(type(map_df))

# Plot the default map
map_df.plot()

# Join both the DataFrames by state names

merged = map_df.set_index('st_nm').join(csv_df.set_index('State'))
merged

# Detect missing values. Return a boolean same-sized object indicating if the values are NA

merged.isna().sum()

# Summary to get the max and min and other statistical data on the dataset

merged.describe()


def truncate_colormap(cmap, minval=0.0, maxval=1.0, n=100):
    new_cmap = colors.LinearSegmentedColormap.from_list(
        'trunc({n},{a:.2f},{b:.2f})'.format(n=cmap.name, a=minval, b=maxval),
        cmap(np.linspace(minval, maxval, n)))
    return new_cmap

arr = np.linspace(0, 50, 100).reshape((10, 10))
fig, ax = plt.subplots(ncols=2)

cmap = plt.get_cmap('RdPu')
new_cmap = truncate_colormap(cmap, 0.3, 1)

ax[0].imshow(arr, interpolation='nearest', cmap=cmap)
ax[1].imshow(arr, interpolation='nearest', cmap=new_cmap)
plt.show()

# create figure and axes for Matplotlib and set the title
fig, ax = plt.subplots(1, figsize=(10, 6))
ax.axis('off')
ax.set_title('Percent of responders who know English', fontdict={'fontsize': '15', 'fontweight' : '3'})

# plot the figure
merged.plot(column='Percent of responders who know english', 
            cmap= new_cmap, 
            linewidth=0.9, 
          ax=ax, edgecolor='1',
          legend=True, missing_kwds={
          "color": "lightgrey",
          "label": "Missing values",
    },)

fig.savefig("State_wise_english_fin.png", dpi=100)

