import streamlit as st
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/giswqs/leafmap/master/examples/data/us_cities.csv')
st.map(df)
