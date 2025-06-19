import os
from dotenv import load_dotenv

load_dotenv()

PROJECT_ID = os.getenv("PROJECT_ID")
BQ_DATASET = os.getenv("DATASET_ID")
BQ_TABLE = os.getenv("TABLE_ID")
API_KEY = os.getenv("AVIATIONSTACK_API_KEY")  # ✅ Add this line

# Validate
if not all([PROJECT_ID, BQ_DATASET, BQ_TABLE, API_KEY]):
    raise ValueError("❌ Missing one or more required environment variables.")
