import duckdb
from src.extract import read_local_csv
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
        WHEN age < 18 THEN 'lt18'
        WHEN age <= 30 THEN '18-30'
        WHEN age <= 50 THEN '31-50'
        WHEN age <= 70 THEN '51-70'
        ELSE '70+'
    END AS age_Bucket
FROM joined
"""

def enrich_orders(orders,customers):
    """
    Enriches the orders data by joining it with customer data and adding an age bucket.

    Args:
        orders (duckdb.DuckDBPyRelation): The orders data.
        customers (duckdb.DuckDBPyRelation): The customers data.
    """
    return duckdb.sql(ENRICH_ORDERS_SQL)

if __name__ == "__main__":
    orders = read_local_csv("data/orders.csv")
    customers = read_local_csv("data/customers.csv")
    enriched_orders = enrich_orders(orders, customers)
    enriched_orders.limit(5).show()
    
    duckdb.sql("SELECT age_Bucket, COUNT(*) AS count FROM enriched_orders GROUP BY 1 ORDER BY 1").show()
    
    print("1) Total enriched rows:")
    duckdb.sql("SELECT COUNT(*) AS total_enriched_rows FROM enriched_orders").show()
    
    print("2) Orders with a missing first_name:")
    duckdb.sql("""SELECT order_id, customer_id, first_name 
               FROM enriched_orders 
               WHERE first_name IS NULL""").show()