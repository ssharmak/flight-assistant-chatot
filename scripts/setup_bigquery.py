import sys
import os

# Ensure the parent directory is in the module path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from google.cloud import bigquery
from google.api_core.exceptions import NotFound, Conflict
from config.settings import PROJECT_ID, BQ_DATASET, BQ_TABLE

client = bigquery.Client()

table_id = f"{PROJECT_ID}.{BQ_DATASET}.{BQ_TABLE}"

# Define the schema
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
    # Check if table exists
    table = client.get_table(table_id)
    print(f"ℹ️ Table already exists: {table_id}")

    # Compare existing schema with the new schema
    existing_fields = {field.name for field in table.schema}
    new_fields = [field for field in schema if field.name not in existing_fields]

    if new_fields:
        updated_schema = table.schema + new_fields
        table.schema = updated_schema
        table = client.update_table(table, ["schema"])
        print("✅ Schema updated with new fields.")
    else:
        print("✅ Table schema already matches.")

except NotFound:
    # If table doesn't exist, create it
    table_ref = bigquery.Table(table_id, schema=schema)
    client.create_table(table_ref)
    print(f"✅ Table created successfully: {table_id}")

except Exception as e:
    print(f"❌ Error during setup: {e}")
