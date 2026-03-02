{{ config(materialized='table') }}

WITH base_updates AS (
    SELECT 
        CASE 
            WHEN stop_id LIKE '%N' OR stop_id LIKE '%S' 
            THEN LEFT(stop_id, LENGTH(stop_id) - 1)
            ELSE stop_id 
        END AS clean_stop_id,
        TIMESTAMP_SECONDS(CAST(arrival_timestamp AS INT64)) AS arrival_time,
        TIMESTAMP_SUB(TIMESTAMP_SECONDS(CAST(arrival_timestamp AS INT64)), INTERVAL 2 MINUTE) AS scheduled_arrival,
        trip_id,
        route_id
    FROM {{ source('mta_raw', 'raw_trip_updates') }}
),

stops_info AS (
    SELECT stop_id, stop_name, stop_lat, stop_lon
    FROM {{ source('mta_raw', 'static_stops') }}
)

SELECT 
    b.trip_id,
    b.route_id,
    s.stop_name,
    b.arrival_time,
    b.scheduled_arrival,
    s.stop_lat,
    s.stop_lon
FROM base_updates AS b
LEFT JOIN stops_info AS s ON b.clean_stop_id = s.stop_id