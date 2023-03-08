import pandas as pd
import geopandas as gpd
import folium
import streamlit as st
from streamlit_folium import folium_static, st_folium
from geographiclib.geodesic import Geodesic
from shapely.geometry import Polygon
from pathlib import Path

from params import *
from data import get_data_with_cache

def main():
    # Config for website
    st.set_page_config(
        page_title= 'Poverty Mapper',
        page_icon="🌍",
        layout = "wide",
        initial_sidebar_state="expanded")

    with st.sidebar:
        st.title('Poverty Mapper')
        # st.header('Select region')
    #     country = st.selectbox(label = 'Country', label_visibility='collapsed',options=('France', 'Italy', 'USA','New Zealand'))
    #     region = st.radio(label='Region', options=('REG01', 'REG02', 'REG03', 'REG04', 'REG05', 'REG06', 'REG07'))


    # st.title('Poverty Mapper')

    tab1, tab2, tab3 = st.tabs(["Target", "Test", "Central African Republic"])

    geod = Geodesic.WGS84
    tile_size = 6720 #in meters

    with tab1:
        query = f"""
            SELECT {",".join(COLUMN_NAMES_RAW)}
            FROM {GCP_PROJECT}.{BQ_DATASET}.DHS_CLUSTERS
            """
        df_cache_path = Path(LOCAL_DATA_PATH).joinpath("DHS_CLUSTERS.csv")
        df = get_data_with_cache(query=query,
                                gcp_project=GCP_PROJECT,
                                cache_path=df_cache_path,
                                data_has_header=True)

        ##############
        # FOR TESTING
        ##############
        # df = df[df['year'] == 2015]
        # df = df[df['country'] == 'angola']
        # df = df[df['GID_1'] == 'AGO.1']
        # st.map(df)

        df['lat_max'] = df.apply(lambda x: geod.Direct(x.lat, x.lon, 0, tile_size/2)['lat2'], axis=1)
        df['lon_max'] = df.apply(lambda x: geod.Direct(x.lat, x.lon, 90, tile_size/2)['lon2'], axis=1)
        df['lat_min'] = df.apply(lambda x: geod.Direct(x.lat, x.lon, 180, tile_size/2)['lat2'], axis=1)
        df['lon_min'] = df.apply(lambda x: geod.Direct(x.lat, x.lon, 270, tile_size/2)['lon2'], axis=1)
        df['geometry'] = df.apply(lambda x: Polygon(zip([x.lon_min, x.lon_max, x.lon_max, x.lon_min],
                                                        [x.lat_min, x.lat_min, x.lat_max, x.lat_max])), axis=1)

        gdf = gpd.GeoDataFrame(df)
        # m = folium.Map(location=[gdf.lat.mean(), gdf.lon.mean()], zoom_start=3)
        m = folium.Map(location=[3, 20], zoom_start=3)

        cm = folium.LinearColormap(["purple", "white", "orange"], caption="Wealthpooled",
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
            tooltip=folium.features.GeoJsonTooltip(["wealthpooled"])
        ).add_to(m)

        st_data = folium_static(m, width = 900)
        # st_data = st_folium(m, width = 1500)

    with tab2:
        query = f"""
            SELECT {",".join(COLUMN_NAMES_RAW)}
            FROM {GCP_PROJECT}.{BQ_DATASET}.DHS_OOC_A_TEST
            """
        test_df_cache_path = Path(LOCAL_DATA_PATH).joinpath("DHS_OOC_A_TEST.csv")
        test_df = get_data_with_cache(query=query,
                                gcp_project=GCP_PROJECT,
                                cache_path=test_df_cache_path,
                                data_has_header=True)

        test_df['lat_max'] = test_df.apply(lambda x: geod.Direct(x.lat, x.lon, 0, tile_size/2)['lat2'], axis=1)
        test_df['lon_max'] = test_df.apply(lambda x: geod.Direct(x.lat, x.lon, 90, tile_size/2)['lon2'], axis=1)
        test_df['lat_min'] = test_df.apply(lambda x: geod.Direct(x.lat, x.lon, 180, tile_size/2)['lat2'], axis=1)
        test_df['lon_min'] = test_df.apply(lambda x: geod.Direct(x.lat, x.lon, 270, tile_size/2)['lon2'], axis=1)
        test_df['geometry'] = test_df.apply(lambda x: Polygon(zip([x.lon_min, x.lon_max, x.lon_max, x.lon_min],
                                                        [x.lat_min, x.lat_min, x.lat_max, x.lat_max])), axis=1)

        test_gdf = gpd.GeoDataFrame(test_df)
        # test_m = folium.Map(location=[test_gdf.lat.mean(), test_gdf.lon.mean()], zoom_start=3)
        test_m = folium.Map(location=[3, 20], zoom_start=3)

        test_cm = folium.LinearColormap(["purple", "white", "orange"], caption="Wealthpooled",
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
            tooltip=folium.features.GeoJsonTooltip(["wealthpooled"])
        ).add_to(test_m)

        st_data = folium_static(test_m, width = 900)

    with tab3:
        query = f"""
            SELECT {",".join(['country', 'year', 'city', 'lat', 'lon', 'wealthpooled'])}
            FROM {GCP_PROJECT}.{BQ_DATASET}.CAR_PRED
            """
        car_df_cache_path = Path(LOCAL_DATA_PATH).joinpath("CAR_PRED.csv")
        car_df = get_data_with_cache(query=query,
                                gcp_project=GCP_PROJECT,
                                cache_path=car_df_cache_path,
                                data_has_header=True)

        car_df['lat_max'] = car_df.apply(lambda x: geod.Direct(x.lat, x.lon, 0, tile_size*10/2)['lat2'], axis=1)
        car_df['lon_max'] = car_df.apply(lambda x: geod.Direct(x.lat, x.lon, 90, tile_size*10/2)['lon2'], axis=1)
        car_df['lat_min'] = car_df.apply(lambda x: geod.Direct(x.lat, x.lon, 180, tile_size*10/2)['lat2'], axis=1)
        car_df['lon_min'] = car_df.apply(lambda x: geod.Direct(x.lat, x.lon, 270, tile_size*10/2)['lon2'], axis=1)
        car_df['geometry'] = car_df.apply(lambda x: Polygon(zip([x.lon_min, x.lon_max, x.lon_max, x.lon_min],
                                                        [x.lat_min, x.lat_min, x.lat_max, x.lat_max])), axis=1)

        car_gdf = gpd.GeoDataFrame(car_df)
        # car_m = folium.Map(location=[car_gdf.lat.mean(), car_gdf.lon.mean()], zoom_start=3)
        car_m = folium.Map(location=[3, 20], zoom_start=3)

        car_cm = folium.LinearColormap(["purple", "white", "orange"], caption="Wealthpooled",
                                vmin=min(car_gdf['wealthpooled']), vmax=max(car_gdf['wealthpooled']))

        style_function = lambda feature: {
            "fillColor": car_cm(feature["properties"]["wealthpooled"]),
            "fillOpacity": 0.8,
            "weight": 0.8,
            "color": car_cm(feature["properties"]["wealthpooled"]),
        }

        #Add the colormap as a legend
        car_cm.add_to(car_m)

        folium.GeoJson(
            car_gdf.__geo_interface__,
            style_function=style_function,
            tooltip=folium.features.GeoJsonTooltip(["wealthpooled"])
        ).add_to(car_m)

        st_data = folium_static(car_m, width = 900)



if __name__ == '__main__':
    main()
