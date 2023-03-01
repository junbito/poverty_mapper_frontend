import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import folium_static
from geographiclib.geodesic import Geodesic
from shapely.geometry import Polygon

df = pd.read_csv('dhs_clusters.csv')
# df = df[df['year'] == 2015]
# df = df[df['country'] == 'angola']
# df = df[df['GID_1'] == 'AGO.1']
# st.map(df)

geod = Geodesic.WGS84

df['lat_max'] = df.apply(lambda x: geod.Direct(x.lat, x.lon, 0, 67200/2)['lat2'], axis=1)
df['lon_max'] = df.apply(lambda x: geod.Direct(x.lat, x.lon, 90, 67200/2)['lon2'], axis=1)
df['lat_min'] = df.apply(lambda x: geod.Direct(x.lat, x.lon, 180, 67200/2)['lat2'], axis=1)
df['lon_min'] = df.apply(lambda x: geod.Direct(x.lat, x.lon, 270, 67200/2)['lon2'], axis=1)
df['geometry'] = df.apply(lambda x: Polygon(zip([x.lon_min, x.lon_max, x.lon_max, x.lon_min],
                                                [x.lat_min, x.lat_min, x.lat_max, x.lat_max])), axis=1)

gdf = gpd.GeoDataFrame(df, geometry=df.geometry)

m = folium.Map(location=[df.lat.mean(), df.lon.mean()], zoom_start=3, control_scale=True)

for _, r in df.iterrows():
    sim_geo = gpd.GeoSeries(r['geometry']).simplify(tolerance=0.001)
    geo_j = sim_geo.to_json()
    geo_j = folium.GeoJson(data=geo_j,
                           style_function=lambda x: {'fillColor': 'orange'})
    iframe = folium.IFrame(str(r["country"]).capitalize() + ' ' + str(r["wealthpooled"]))
    popup = folium.Popup(iframe, min_width=300, max_width=300, max_height=100).add_to(geo_j)
    geo_j.add_to(m)

st_data = folium_static(m, width=700)
