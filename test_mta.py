import requests
from google.transit import gtfs_realtime_pb2

MTA_URL = "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-ace"
API_KEY = "YOUR_REAL_KEY"

headers = {"x-api-key": API_KEY}

def test_connection():
    response = requests.get(MTA_URL, headers=headers)

    print("Status:", response.status_code)

    if response.status_code == 200:
        print("Successfully connected to MTA!")

        feed = gtfs_realtime_pb2.FeedMessage()
        feed.ParseFromString(response.content)

        for entity in feed.entity:
            if entity.HasField("trip_update"):
                print("\n--- Found a Trip Update! ---")
                print("Route ID:", entity.trip_update.trip.route_id)
                break
    else:
        print("Response content:")
        print(response.text[:500])  # For debugging

if __name__ == "__main__":
    test_connection()