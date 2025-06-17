import pandas as pd
from google.cloud import bigquery
from config.settings import PROJECT_ID, BQ_DATASET, BQ_TABLE

def analyze_weekly_data(start_date=None, end_date=None):
    """
    Fetches and analyzes flight data from BigQuery for the given date range.
    
    Parameters:
        start_date (str): 'YYYY-MM-DD'
        end_date (str): 'YYYY-MM-DD'
        
    Returns:
        pd.DataFrame: Cleaned DataFrame of flights.
    """
    client = bigquery.Client()
    table_id = f"{PROJECT_ID}.{BQ_DATASET}.{BQ_TABLE}"

    query = f"""
        SELECT *
        FROM `{table_id}`
        WHERE flight_date BETWEEN @start_date AND @end_date
        ORDER BY flight_date, scheduled_departure
    """

    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("start_date", "DATE", start_date),
            bigquery.ScalarQueryParameter("end_date", "DATE", end_date),
        ]
    )

    try:
        df = client.query(query, job_config=job_config).to_dataframe()
        return df
    except Exception as e:
        print(f"❌ Failed to fetch data: {e}")
        return pd.DataFrame()
