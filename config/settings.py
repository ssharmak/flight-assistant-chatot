import os
from dotenv import load_dotenv

# Load the .env file from the root directory
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(dotenv_path=env_path)

PROJECT_ID = os.getenv("PROJECT_ID")
BQ_DATASET = os.getenv("BQ_DATASET")
BQ_TABLE = os.getenv("BQ_TABLE")
API_KEY = os.getenv("AVIATIONSTACK_API_KEY")

if not all([PROJECT_ID, BQ_DATASET, BQ_TABLE]):
    raise ValueError("❌ Environment variables PROJECT_ID, BQ_DATASET, or BQ_TABLE are missing.")
