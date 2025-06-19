# 📦 Import environment configuration variables
from config.settings import PROJECT_ID, BQ_DATASET, BQ_TABLE

# ✅ Confirm that environment variables are successfully loaded
print("✅ ENV loaded:")
print("PROJECT_ID:", PROJECT_ID)       # Google Cloud project ID
print("BQ_DATASET:", BQ_DATASET)       # BigQuery dataset ID
print("BQ_TABLE:", BQ_TABLE)           # BigQuery table name
