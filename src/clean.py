import duckdb

DB_PATH = "data/pipeline.duckdb"

CLEAN_ORDERS_SQL = """
CREATE OR REPLACE TABLE orders_clean AS
SELECT * REPLACE (COALESCE(first_name, 'Unknown') AS first_name)
FROM enriched_orders
WHERE price IS NOT NULL
QUALIFY ROW_NUMBER() OVER (PARTITION BY order_id ORDER BY order_date) = 1
"""

REJECTED_ORDERS_SQL = """
CREATE OR REPLACE TABLE orders_rejected AS
SELECT DISTINCT *, 'missing price' AS reject_reason
FROM enriched_orders
WHERE price IS NULL
"""


def clean_orders(con: duckdb.DuckDBPyConnection) -> None:
    """Build orders_clean (publishable) and orders_rejected (quarantine) tables."""
    con.sql(CLEAN_ORDERS_SQL)
    con.sql(REJECTED_ORDERS_SQL)


if __name__ == "__main__":
    con = duckdb.connect(DB_PATH)
    clean_orders(con)
    for table in ("enriched_orders", "orders_clean", "orders_rejected"):
        count = con.sql(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"{table}: {count} rows")
    con.close()