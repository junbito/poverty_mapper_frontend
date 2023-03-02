import os

##################  VARIABLES  ##################
# GCP_PROJECT = os.environ.get("GCP_PROJECT")
# BQ_DATASET = os.environ.get("BQ_DATASET")
GCP_PROJECT = "poverty-mapper-379103"
BQ_DATASET = "poverty_mapper"

##################  CONSTANTS  #####################
LOCAL_DATA_PATH = "dev_data"
COLUMN_NAMES_RAW = ['country', 'year', 'lat', 'lon', 'GID_1', 'GID_2', 'wealthpooled', 'households', 'urban_rural']
