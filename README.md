# NYC MTA Real-Time Transit Data Pipeline

## 🚀 Executive Summary
* The NYC MTA manages millions of daily commutes, yet the complexity of real-time transit data often leaves a "visibility gap" between raw API feeds and actionable operational insights.
* This project bridges that gap by engineering a high-velocity ELT (Extract, Load, Transform) pipeline that functions as a real-time Digital Twin of the Eighth Avenue Line (A, C, E). By ingesting raw Protobuf streams and applying modular dbt transformations, I’ve built an Automated Operations Center that tracks ~30,000 arrival updates per session with sub-minute latency.
* This isn't just a dashboard; it’s a Real-Time Data Audit that identifies bottlenecks, calculates schedule variance at the station level, and proves data freshness through a custom "Heartbeat" monitoring system.

## 🛠️ The Tech Stack
* **Ingestion:** Python (Requests, GTFS-Realtime/Protobuf)
* **Data Warehouse:** Google BigQuery
* **Transformation:** dbt (Data Build Tool)
* **Visualization:** Looker Studio
  
![Flow](Steps.png)

## 🏗️ Architecture & Lineage
The pipeline extracts Protobuf feeds from the MTA API, loads them into BigQuery "Raw" tables, and utilizes **dbt** to sanitize Station IDs and join them with static GTFS data for geospatial mapping.

## 💡 Key Engineering Challenges & Solutions
### 1. The ID Mismatch Problem
**Challenge:** Real-time feeds use dynamic `stop_id` suffixes (N/S) that do not exist in static schedule files, causing join failures.
**Solution:** Engineered a dbt transformation layer using Regex to strip suffixes, ensuring a 100% match rate between live trips and physical station coordinates.

### 2. Custom Business Logic
I implemented custom SQL logic in the BI layer to define system health:
* **On Time:** Arrivals within a 5-minute variance of the scheduled time.
* **Slight Delay:** 5–10 minutes.
* **Delayed:** 10–20 minutes.
* **Major Delay:** > 20 minutes (verified by your average delay scorecard of 48.6 min).

## 📊 Dashboard Insights
The final dashboard provides a "Transit Operations Center" view of the NYC subway system:
* **Real-Time Fleet Map:** Live geospatial tracking of active trips.
* **Service Reliability:** KPI scorecards measuring On-Time Performance (OTP).
* **Traffic Analysis:** Identification of system bottlenecks at high-traffic stations like 42 St-Port Authority.
* **Data Freshness Audit:** A real-time scatter plot proving sub-minute ingestion pulses from the MTA API to BigQuery.

## 📊 Live Dashboard
[**Click here to view the Live NYC MTA Operational Dashboard**](https://lookerstudio.google.com/s/spKzCEr5uZ0)

## 🏗️ Technical Architecture Refinement
* **Line Coverage:** Specifically engineered to monitor the Eighth Avenue Line (A, C, E), handling the high-velocity data surges unique to the Manhattan trunk lines.
