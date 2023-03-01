import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import st_folium, folium_static
from geographiclib.geodesic import Geodesic
from shapely.geometry import Polygon


# df = pd.read_csv('https://raw.githubusercontent.com/giswqs/leafmap/master/examples/data/us_cities.csv')
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
df['geometry'] = df.apply(lambda x: Polygon(zip([x.lon_min, x.lon_max, x.lon_max, x.lon_min], [x.lat_min, x.lat_min, x.lat_max, x.lat_max])), axis=1)

gdf = gpd.GeoDataFrame(df, geometry=df.geometry)

m = folium.Map(location=[df.lat.mean(), df.lon.mean()], zoom_start=3, control_scale=True)

for _, r in df.iterrows():
    # Without simplifying the representation,
    # the map might not be displayed
    sim_geo = gpd.GeoSeries(r['geometry']).simplify(tolerance=0.001)
    geo_j = sim_geo.to_json()
    geo_j = folium.GeoJson(data=geo_j,
                           style_function=lambda x: {'fillColor': 'orange'})
    # folium.Popup(r['wealthpooled']).add_to(geo_j)
    iframe = folium.IFrame(str(r["country"]).capitalize() + ' ' + str(r["wealthpooled"]))
    popup = folium.Popup(iframe, min_width=300, max_width=300, max_height=100).add_to(geo_j)
    geo_j.add_to(m)

st_data = folium_static(m, width=700)

# m = folium.Map(location=[df.lat.mean(), df.lon.mean()], zoom_start=3, control_scale=True)

# geod = Geodesic.WGS84
# shapesLayer = folium.FeatureGroup(name="Vector Shapes").add_to(m)

# #Loop through each row in the dataframe
# for i, row in df.iterrows():
#     #Setup the content of the popup
#     iframe = folium.IFrame('Wealth: ' + str(row["wealthpooled"]))

#     #Initialise the popup using the iframe
#     popup = folium.Popup(iframe, min_width=300, max_width=300)

#     #Add each row to the map
#     folium.Marker(location=[row['lat'],row['lon']], popup = popup, c=row['wealthpooled']).add_to(m)

#     g = geod.Direct(row['lat'], row['lon'], 0, 67200/2)
#     lat_max = g['lat2']
#     g = geod.Direct(row['lat'], row['lon'], 90, 67200/2)
#     lon_max = g['lon2']
#     g = geod.Direct(row['lat'], row['lon'], 180, 67200/2)
#     lat_min = g['lat2']
#     g = geod.Direct(row['lat'], row['lon'], 270, 67200/2)
#     lon_min = g['lon2']

#     folium.Rectangle([(lat_min, lon_min), (lat_max, lon_max)],
#                     color="green",
#                     weight=2,
#                     fill=True,
#                     fill_color="pink",
#                     fill_opacity=0.5).add_to(shapesLayer)

# folium.LayerControl().add_to(m)

# # st_data = st_folium(m, width=700)
# st_data = folium_static(m, width=700)

# import plotly.express as px

# fig = px.scatter_mapbox(df, lat="lat", lon="lon", hover_name='wealthpooled', zoom=3)

# geod = Geodesic.WGS84

# fig.update_layout(mapbox_style="open-street-map")
# fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

# def get_polygon(lons, lats, color='blue'):
#     if len(lons) != len(lats):
#         raise ValueError('the legth of longitude list  must coincide with that of latitude')
#     geojd = {"type": "FeatureCollection"}
#     geojd['features'] = []
#     coords = []
#     for lon, lat in zip(lons, lats):
#         coords.append((lon, lat))
#     coords.append((lons[0], lats[0]))  #close the polygon
#     geojd['features'].append({ "type": "Feature",
#                                "geometry": {"type": "Polygon",
#                                             "coordinates": [coords] }})
#     layer=dict(sourcetype = 'geojson',
#              source =geojd,
#              below='',
#              type = 'fill',
#              color = color)
#     return layer

# mylayers =[]

# #Loop through each row in the dataframe
# for i, row in df.iterrows():
#     g = geod.Direct(row['lat'], row['lon'], 0, 67200/2)
#     lat_max = g['lat2']
#     g = geod.Direct(row['lat'], row['lon'], 90, 67200/2)
#     lon_max = g['lon2']
#     g = geod.Direct(row['lat'], row['lon'], 180, 67200/2)
#     lat_min = g['lat2']
#     g = geod.Direct(row['lat'], row['lon'], 270, 67200/2)
#     lon_min = g['lon2']
#     # mylayers.append(get_polygon(lons=[14, 16, 16, 14], lats=[58.55, 58.55, 60.6, 60.6],  color='gold'))
#     mylayers.append(get_polygon(lons=[lon_min, lon_max, lon_max, lon_min], lats=[lat_min, lat_min, lat_max, lat_max],  color='gold'))


# fig.layout.update(mapbox_layers =mylayers);

# st.plotly_chart(fig)
