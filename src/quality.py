import sys
import duckdb

DB_PATH = "data/pipeline.duckdb"

# Each check counts the rows that break a rule. 0 means the check passes.

ORDER_CHECKS = {
    "order_id is unique": "SELECT COUNT(*) - COUNT(DISTINCT order_id) FROM {table}",
    "first_name is not null": "SELECT COUNT(*) FROM {table} WHERE first_name IS NULL",
    "price is not null": "SELECT COUNT(*) FROM {table} WHERE price IS NULL",
    "price is positive": "SELECT COUNT(*) FROM {table} WHERE price <= 0",
}

def run_checks(con: duckdb.DuckDBPyConnection, table: str, checks: dict) -> list[tuple]:
    """Run each check against `table` and return (check_name, failing_rows) pairs."""
    results = []
    for name, sql in checks.items():
        failing_rows = con.sql(sql.format(table=table)).fetchone()[0]
        results.append((name, failing_rows))
    return results

def print_report(table: str, results: list[tuple]) -> bool:
    """
    Print a report of the quality checks for a given table.

    Args:
        table (str): The name of the table being checked.
        results (list[tuple]): A list of tuples containing the check description and the count of violations.

    Returns:
        bool: True if all checks passed (i.e., all counts are 0), False otherwise.
    """
    print(f"Quality checks for {table}:")
    print("-" * 50)
    for name, failing_rows in results:
        status = "PASS" if failing_rows == 0 else "FAIL"
        print(f"{status} {name:<28} failing rows: {failing_rows}")
    return all(failing_rows == 0 for _, failing_rows in results)


if __name__ == "__main__":
    table = sys.argv[1] if len(sys.argv) > 1 else "enriched_orders"
    con = duckdb.connect(DB_PATH, read_only=True)
    results = run_checks(con, table, ORDER_CHECKS)
    con.close()

    all_passed = print_report(table, results)
    sys.exit(0 if all_passed else 1)