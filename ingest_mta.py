import os
import requests
import time
from google.transit import gtfs_realtime_pb2
from google.cloud import bigquery

# --- CONFIGURATION ---
# The Open URL you confirmed works with a 200 status
MTA_URL = "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-ace"

# GCP Configuration from your screenshots
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service-account.json"
PROJECT_ID = "mta-transit-project-488901" 
TABLE_ID = f"{PROJECT_ID}.mta_data.raw_trip_updates"

client = bigquery.Client()

def fetch_mta_data():
    try:
        print(f"[{time.strftime('%H:%M:%S')}] Fetching Open MTA Data...")
        response = requests.get(MTA_URL, timeout=15)
        response.raise_for_status()
        
        feed = gtfs_realtime_pb2.FeedMessage()
        feed.ParseFromString(response.content)
        
        rows = []
        for entity in feed.entity:
            if entity.HasField('trip_update'):
                trip = entity.trip_update.trip
                for update in entity.trip_update.stop_time_update:
                    arrival_time = update.arrival.time if update.arrival.time else update.departure.time
                    if arrival_time:
                        rows.append({
                            "trip_id": str(trip.trip_id),
                            "route_id": str(trip.route_id),
                            "stop_id": str(update.stop_id),
                            "arrival_timestamp": int(arrival_time),
                            "ingested_at": int(time.time())
                        })
        return rows
    except Exception as e:
        print(f"⚠️ Fetch Error: {e}")
        return []

def batch_load_to_bigquery(rows):
    """Sandbox-friendly: Uses a Load Job instead of Streaming."""
    if not rows:
        return
    
    # Setup job to append data (don't overwrite old data)
    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_APPEND",
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
    )

    print(f"Attempting Batch Load of {len(rows)} rows...")
    
    # This specific method is free-tier compatible
    try:
        job = client.load_table_from_json(rows, TABLE_ID, job_config=job_config)
        job.result() # Wait for the upload to finish
        print("✅ SUCCESS: Data is now in BigQuery.")
    except Exception as e:
        print(f"❌ BigQuery Load Error: {e}")

if __name__ == "__main__":
    print("Starting Sandbox-Friendly Ingestion... (Ctrl+C to stop)")
    while True:
        data = fetch_mta_data()
        if data:
            batch_load_to_bigquery(data)
        
        # We'll wait 2 minutes between batches to stay safe in the Sandbox
        print("Waiting 120 seconds for next batch...")
        time.sleep(120)