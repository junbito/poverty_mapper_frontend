import geopandas as gpd
import folium


def get_map(gdf:gpd.GeoDataFrame,
            lat=None,
            lon=None,
            zoom_start=4,
            cmap_min=None,
            cmap_max=None) -> folium.Map:

    if not lat:
        lat = gdf.lat.mean()
    if not lon:
        lon = gdf.lon.mean()
    if not cmap_min:
        cmap_min = min(gdf['wealthpooled'])
    if not cmap_max:
        cmap_max = max(gdf['wealthpooled'])

    map = folium.Map(location=[lat, lon], zoom_start=zoom_start)

    color_map = folium.LinearColormap(["purple", "green", "orange"],
                                      caption="Wealthpooled",
                                      vmin=cmap_min, vmax=cmap_max)

    style_function = lambda feature: {
        "fillColor": color_map(feature["properties"]["wealthpooled"]),
        "fillOpacity": 0.8,
        "weight": 0.8,
        "color": color_map(feature["properties"]["wealthpooled"]),
    }

    #Add the colormap as a legend
    color_map.add_to(map)

    folium.GeoJson(
        gdf.__geo_interface__,
        style_function=style_function,
        tooltip=folium.features.GeoJsonTooltip(["country", "year", "wealthpooled"])
    ).add_to(map)

    folium.TileLayer('cartodbpositron').add_to(map)

    return map
