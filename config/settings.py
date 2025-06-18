import os
from dotenv import load_dotenv

load_dotenv()

PROJECT_ID = os.getenv("PROJECT_ID")
BQ_DATASET = os.getenv("DATASET_ID")  # Use DATASET_ID not BQ_DATASET
BQ_TABLE = os.getenv("TABLE_ID")

if not all([PROJECT_ID, BQ_DATASET, BQ_TABLE]):
    raise ValueError("❌ Environment variables PROJECT_ID, DATASET_ID, or TABLE_ID are missing.")
