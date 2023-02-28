import os

##################  VARIABLES  ##################
GCP_PROJECT = os.environ.get("GCP_PROJECT")
BQ_DATASET = os.environ.get("BQ_DATASET")

##################  CONSTANTS  ##################
LOCAL_DATA_PATH = "data"
COLUMN_NAMES_RAW = ['country', 'year', 'city', 'lat', 'lon', 'wealthpooled']
