import streamlit as st
from streamlit_folium import folium_static

from params import *
from data import get_data_with_cache
from map import get_map


def main():
    # Config for website
    st.set_page_config(
        page_title= 'Poverty Mapper',
        page_icon="🌍",
        layout = "wide")

    st.title('Poverty Mapper')

    tab1, tab2, tab3 = st.tabs(["SURVEY DATASET", "TEST", "PREDICTIONS"])

    with tab1:
        target_gdf = get_data_with_cache(table_name='DHS_CLUSTERS')
        target_map = get_map(gdf=target_gdf)
        st_data = folium_static(target_map, width = 900)

    with tab2:
        test_gdf = get_data_with_cache(table_name='DHS_OOC_A_TEST')
        test_map = get_map(gdf=test_gdf, lat=target_gdf.lat.mean(), lon=target_gdf.lon.mean())
        st_data = folium_static(test_map, width = 900)

    with tab3:
        prediction_gdf = get_data_with_cache(table_name='CAR_PRED')
        prediction_map = get_map(gdf=prediction_gdf, lat=target_gdf.lat.mean(), lon=target_gdf.lon.mean())
        st_data = folium_static(prediction_map, width = 900)


if __name__ == '__main__':
    main()
