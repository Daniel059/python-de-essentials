import duckdb
import pandas as pd
from src.extract import fetch_weather, read_local_csv

ENRICH_ORDERS_SQL = """
WITH joined AS(
SELECT 
    o.*,
    c.first_name,
    c.last_name,
    c.county,
    date_sub('year',c.date_of_birth, current_date) AS age
FROM orders AS o
LEFT JOIN customers AS c 
    ON o.customer_id = c.customer_id
)
SELECT 
    *,
    CASE
        WHEN age IS NULL THEN 'unknown'
        WHEN age < 18 THEN 'lt18'
        WHEN age <= 30 THEN '18-30'
        WHEN age <= 50 THEN '31-50'
        WHEN age <= 70 THEN '51-70'
        ELSE '70+'
    END AS age_bucket
FROM joined
"""
WEATHER_SQL = """
SELECT
    id AS station_id,
    CAST(strptime(date, '%Y%m%d') AS DATE) AS observation_date,
    CAST(value AS INTEGER) / 10.0 AS precipitation_mm
FROM weather_df
WHERE element = 'PRCP'
  AND qflag = ''
"""

def enrich_orders(orders,customers):
    """
    Enriches the orders data by joining it with customer data and adding an age bucket.

    Args:
        orders (duckdb.DuckDBPyRelation): The orders data.
        customers (duckdb.DuckDBPyRelation): The customers data.
    """
    return duckdb.sql(ENRICH_ORDERS_SQL)

def transform_weather(weather_rows):
    """
    Clean NOAA daily precipitation readings.

    Args:
        weather_rows (list[dict]): Raw rows from fetch_weather().
    Returns:
        duckdb.DuckDBPyRelation: station_id, observation_date, precipitation_mm.
    """
    weather_df = pd.DataFrame(weather_rows)
    return duckdb.sql(WEATHER_SQL)

if __name__ == "__main__":
    orders = read_local_csv("data/orders.csv")
    customers = read_local_csv("data/customers.csv")
    enriched_orders = enrich_orders(orders, customers)
    enriched_orders.limit(5).show()

    weather = transform_weather(fetch_weather())
    weather.limit(5).show()

    print("Weather sanity checks:")
    duckdb.sql("""
        SELECT
            MIN(observation_date)            AS first_day,
            MAX(observation_date)            AS last_day,
            COUNT(*)                         AS rows,
            COUNT(DISTINCT observation_date) AS distinct_days,
            MAX(precipitation_mm)            AS max_mm,
            MIN(precipitation_mm)            AS min_mm
        FROM weather
    """).show()
