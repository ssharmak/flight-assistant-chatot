import os
import sys

# Ensure the root path is included
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(parent_dir)

from dotenv import load_dotenv
load_dotenv()

from google.cloud import bigquery
from google.api_core.exceptions import NotFound
from config.settings import PROJECT_ID, BQ_DATASET, BQ_TABLE

# Validate .env variables
if not all([PROJECT_ID, BQ_DATASET, BQ_TABLE]):
    raise EnvironmentError(f"❌ Missing environment variables. Loaded: "
                           f"PROJECT_ID={PROJECT_ID}, BQ_DATASET={BQ_DATASET}, BQ_TABLE={BQ_TABLE}")

client = bigquery.Client(project=PROJECT_ID)
table_id = f"{PROJECT_ID}.{BQ_DATASET}.{BQ_TABLE}"

# Define schema
schema = [
    bigquery.SchemaField("flight_date", "DATE"),
    bigquery.SchemaField("airline_name", "STRING"),
    bigquery.SchemaField("flight_number", "STRING"),
    bigquery.SchemaField("departure_airport", "STRING"),
    bigquery.SchemaField("arrival_airport", "STRING"),
    bigquery.SchemaField("status", "STRING"),
    bigquery.SchemaField("scheduled_departure", "TIMESTAMP"),
    bigquery.SchemaField("scheduled_arrival", "TIMESTAMP"),
]

try:
    # Try getting the table to check if it already exists
    table = client.get_table(table_id)
    print(f"ℹ️ Table already exists: {table_id}")

    # Check for schema mismatch and update if needed
    existing_fields = {field.name for field in table.schema}
    new_fields = [field for field in schema if field.name not in existing_fields]

    if new_fields:
        updated_schema = table.schema + new_fields
        table.schema = updated_schema
        client.update_table(table, ["schema"])
        print("✅ Table schema updated.")
    else:
        print("✅ Table schema already matches.")

except NotFound:
    # Table doesn't exist: create it
    table = bigquery.Table(table_id, schema=schema)
    client.create_table(table)
    print(f"✅ Table created successfully: {table_id}")

except Exception as e:
    print(f"❌ Error during setup: {e}")
