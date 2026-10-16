import duckdb
import pandas as pd

from src.extract import fetch_pokemon_details, fetch_weather, read_local_csv
from src.transform import enrich_orders, transform_weather

DB_PATH = "data/pipeline.duckdb"

def load_tables(tables: dict, db_path: str = DB_PATH) -> None:
    """
    Load tables into a DuckDB database.

    Args:
        tables (dict): A dictionary where keys are table names and values are DuckDB relations/DataFrames.
        db_path (str): The path to the DuckDB database file. Default is "data/pipeline.duckdb".
    """
    # Quote the db_path in the ATTACH query
    duckdb.sql(f"ATTACH '{db_path}' AS warehouse")
    
    try:
        for table_name, data in tables.items():
            duckdb.sql(
                f"CREATE OR REPLACE TABLE warehouse.{table_name} AS SELECT * FROM data"
            )
    finally:
        # Detach outside the loop after all tables are loaded
        duckdb.sql("DETACH warehouse")
        

if __name__ == "__main__":
    
    orders = read_local_csv("data/orders.csv")
    customers = read_local_csv("data/customers.csv")
    
    tables = {
        "enriched_orders": enrich_orders(orders, customers),
        "weather_daily": transform_weather(fetch_weather()),
        "pokemon":pd.DataFrame(fetch_pokemon_details())
    }
    load_tables(tables)
    
    # verify by reading back from the file with a fresh connection
    con = duckdb.connect(DB_PATH, read_only=True)
    print(con.sql("SHOW TABLES"))
    
    for name in tables:
        print(name, con.sql(f"SELECT COUNT(*) AS n FROM {name}").fetchone()[0], "rows")
    con.close()