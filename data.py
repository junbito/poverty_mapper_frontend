import pandas as pd
from google.cloud import bigquery
from pathlib import Path
import streamlit as st
from google.oauth2 import service_account

# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def get_data_with_cache(gcp_project:str,
                        query:str,
                        cache_path:Path,
                        data_has_header=True) -> pd.DataFrame:
    """
    Retrieve `query` data from Big Query, or from `cache_path` if file exists.
    Store at `cache_path` if retrieved from Big Query for future re-use.
    """

    if cache_path.is_file():
        # Load data from local CSV
        df = pd.read_csv(cache_path, header='infer' if data_has_header else None)

    else:
        # Create API client.
        credentials = service_account.Credentials.from_service_account_info(
            st.secrets["gcp_service_account"]
        )
        client = bigquery.Client(credentials=credentials)

        # Load data from Querying Big Query server
        query_job = client.query(query)
        result = query_job.result()
        df = result.to_dataframe()

        # Store as CSV if BQ query returned at least one valid line
        if df.shape[0] > 1:
            df.to_csv(cache_path, header=data_has_header, index=False)

    print(f"✅ Data loaded, with shape {df.shape}")

    return df
