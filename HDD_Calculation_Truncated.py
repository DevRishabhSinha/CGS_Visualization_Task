import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('output.csv')
df_2020 = df[df['year'] == 2020]

gdf = gpd.read_file('tl_2020_us_zcta520.shp')
gdf['ZCTA5CE20'] = gdf['ZCTA5CE20'].astype(float)

merged = gdf.set_index('ZCTA5CE20').join(df_2020.set_index('ZIP Code'))

fig, ax = plt.subplots(1, 1, figsize=(10, 10))
merged.plot(column='Weighted Average HDD', cmap='YlOrRd', legend=True, ax=ax, missing_kwds={"color": "lightgrey"})

ax.set_title('Weighted Average HDD for 2020')
ax.set_xlim([-81.4, -78.8])
ax.set_ylim([35, 36.75])

plt.show()