import folium
import streamlit as st
from streamlit_folium import folium_static

from params import *
from data import get_data_with_cache

def main():
    # Config for website
    st.set_page_config(
        page_title= 'Poverty Mapper',
        page_icon="🌍",
        layout = "wide",
        initial_sidebar_state="expanded")

    ##############
    # TAB 1
    ##############
    gdf = get_data_with_cache(table_name='DHS_CLUSTERS')

    m = folium.Map(location=[gdf.lat.mean(), gdf.lon.mean()], zoom_start=4)

    cm = folium.LinearColormap(["purple", "green", "orange"], caption="Wealthpooled",
                            vmin=min(gdf['wealthpooled']), vmax=max(gdf['wealthpooled']))

    style_function = lambda feature: {
        "fillColor": cm(feature["properties"]["wealthpooled"]),
        "fillOpacity": 0.8,
        "weight": 0.8,
        "color": cm(feature["properties"]["wealthpooled"]),
    }

    #Add the colormap as a legend
    cm.add_to(m)

    folium.GeoJson(
        gdf.__geo_interface__,
        style_function=style_function,
        tooltip=folium.features.GeoJsonTooltip(["country", "year", "wealthpooled"])
    ).add_to(m)

    folium.TileLayer('cartodbpositron').add_to(m)

    ##############
    # TAB 2
    ##############
    test_gdf = get_data_with_cache(table_name='DHS_OOC_A_TEST')

    test_m = folium.Map(location=[gdf.lat.mean(), gdf.lon.mean()], zoom_start=4)

    test_cm = folium.LinearColormap(["purple", "green", "orange"], caption="Wealthpooled",
                            vmin=min(test_gdf['wealthpooled']), vmax=max(test_gdf['wealthpooled']))

    style_function = lambda feature: {
        "fillColor": test_cm(feature["properties"]["wealthpooled"]),
        "fillOpacity": 0.8,
        "weight": 0.8,
        "color": test_cm(feature["properties"]["wealthpooled"]),
    }

    #Add the colormap as a legend
    test_cm.add_to(test_m)

    folium.GeoJson(
        test_gdf.__geo_interface__,
        style_function=style_function,
        tooltip=folium.features.GeoJsonTooltip(["country", "year", "wealthpooled"])
    ).add_to(test_m)

    folium.TileLayer('cartodbpositron').add_to(test_m)

    ##############
    # TAB 3
    ##############
    car_gdf = get_data_with_cache(table_name='CAR_PRED')

    car_m = folium.Map(location=[gdf.lat.mean(), gdf.lon.mean()], zoom_start=4)

    car_cm = folium.LinearColormap(["purple", "green", "orange"], caption="Wealthpooled",
                            vmin=min(car_gdf['wealthpooled']), vmax=max(car_gdf['wealthpooled']))

    style_function = lambda feature: {
        "fillColor": car_cm(feature["properties"]["wealthpooled"]),
        "fillOpacity": 0.8,
        "weight": 0.8,
        "color": car_cm(feature["properties"]["wealthpooled"])
    }

    #Add the colormap as a legend
    car_cm.add_to(car_m)

    folium.GeoJson(
        car_gdf.__geo_interface__,
        style_function=style_function,
        tooltip=folium.features.GeoJsonTooltip(["country", "year", "wealthpooled"])
    ).add_to(car_m)

    folium.TileLayer('cartodbpositron').add_to(car_m)

    st.title('Poverty Mapper')

    tab1, tab2, tab3 = st.tabs(["SURVEY DATASET", "TEST", "PREDICTIONS"])

    with tab1:

        st_data = folium_static(m, width = 900)

    with tab2:

        st_data = folium_static(test_m, width = 900)

    with tab3:

        st_data = folium_static(car_m, width = 900)



if __name__ == '__main__':
    main()
