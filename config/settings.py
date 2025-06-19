import os
from dotenv import load_dotenv  # Load environment variables from a .env file

# Load all key-value pairs from the .env file into environment variables
load_dotenv()

# Fetch required environment variables used across the project
PROJECT_ID = os.getenv("PROJECT_ID")               # GCP Project ID
BQ_DATASET = os.getenv("DATASET_ID")               # BigQuery dataset name
BQ_TABLE = os.getenv("TABLE_ID")                   # BigQuery table name
API_KEY = os.getenv("AVIATIONSTACK_API_KEY")       # Aviationstack API key for fetching live flight data

# Validate all required environment variables are set, otherwise raise an error
if not all([PROJECT_ID, BQ_DATASET, BQ_TABLE, API_KEY]):
    raise ValueError("❌ Missing one or more required environment variables.")
