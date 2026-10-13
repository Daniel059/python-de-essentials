import csv 
import random 
from datetime import date, timedelta
from pathlib import Path

random.seed(42)  # For reproducibility: same "random" data every time the script is run
DATA_DIR = Path("data")
COUNTIES = ["Nairobi", "Mombasa", "Kisumu", "Nakuru", "Machakos", "Kiambu", "Eldoret"]
FIRST_NAMES = ["Wanjiku", "Otieno", "Achieng", "Njeri", "Mutiso", "Lemayan", "Wafula"]
LAST_NAMES = ["Kamau", "Ojwang", "Awuor", "Maina","Muli", "Leshan","Simiyu"]
PAYMENT_METHODS = ["M-pesa", "Card", "Cash"]
def random_date(start: date, end: date) -> date:
    return start + timedelta(days=random.randint(0, (end - start).days))

def generate_customers(n: int=50) -> list[dict]:
    customers = [{
      "customer_id":i,
        "first_name":random.choice(FIRST_NAMES),
        "last_name":random.choice(LAST_NAMES),
        "date_of_birth":random_date(date(1950, 1, 1), date(2012, 12, 31)).isoformat(),
        "county":random.choice(COUNTIES)
    }
        for i in range(1, n+1)
    ]
    for customer in random.sample(customers, 3):
        customer["first_name"] = ""
    return customers

def generate_orders(n: int = 200, n_customers: int = 50) -> list[dict]:
    orders = [
        {
            "order_id": i,
            "customer_id": random.randint(1, n_customers),
            "price": random.randint(100, 20000),  # Kenyan shillings
            "order_date": random_date(date(2026, 1, 1), date(2026, 9, 30)).isoformat(),
            "payment_method": random.choice(PAYMENT_METHODS),
        }
        for i in range(1, n + 1)
    ]
    for order in random.sample(orders, 5):  # dirty: 5 missing prices
        order["price"] = ""
    orders.extend(random.sample(orders, 10))  # dirty: 10 duplicated orders
    return orders

def write_csv(path: Path, rows: list[dict]) -> None:
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
        


if __name__ == "__main__":
    DATA_DIR.mkdir(exist_ok=True)
    customers = generate_customers()
    orders = generate_orders()
    write_csv(DATA_DIR / "customers.csv", customers)
    write_csv(DATA_DIR / "orders.csv", orders)
    print(f"Wrote {len(customers)} customers and {len(orders)} orders to {DATA_DIR.resolve()}")