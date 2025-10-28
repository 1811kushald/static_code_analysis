import json
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    filename="inventory.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s]: %(message)s"
)

# Global variable
stock_data = {}


def add_item(item="default", qty=0, logs=None):
    """Add an item to the stock with quantity validation."""
    if logs is None:
        logs = []
    if not isinstance(item, str) or not isinstance(qty, (int, float)):
        logging.warning(f"Invalid input types: item={item}, qty={qty}")
        return

    stock_data[item] = stock_data.get(item, 0) + qty
    log_message = f"{datetime.now()}: Added {qty} of {item}"
    logs.append(log_message)
    logging.info(log_message)


def remove_item(item, qty):
    """Remove items safely from stock."""
    try:
        stock_data[item] -= qty
        if stock_data[item] <= 0:
            del stock_data[item]
    except KeyError:
        logging.error(f"Tried to remove non-existing item: {item}")
    except Exception as e:
        logging.error(f"Unexpected error removing item {item}: {e}")


def get_qty(item):
    """Return current quantity of the item."""
    return stock_data.get(item, 0)


def load_data(file="inventory.json"):
    """Load inventory data from JSON file."""
    global stock_data
    try:
        with open(file, "r", encoding="utf-8") as f:
            stock_data = json.load(f)
    except FileNotFoundError:
        logging.warning(f"{file} not found, starting with empty stock.")
        stock_data = {}


def save_data(file="inventory.json"):
    """Save inventory data to JSON file."""
    with open(file, "w", encoding="utf-8") as f:
        json.dump(stock_data, f, indent=2)


def print_data():
    """Print all inventory items."""
    print("Items Report")
    for i, q in stock_data.items():
        print(f"{i} -> {q}")


def check_low_items(threshold=5):
    """Check and return items below threshold quantity."""
    return [i for i, q in stock_data.items() if q < threshold]


def main():
    add_item("apple", 10)
    add_item("banana", -2)
    add_item(123, "ten")  # Invalid input now safely logged
    remove_item("apple", 3)
    remove_item("orange", 1)
    print(f"Apple stock: {get_qty('apple')}")
    print(f"Low items: {check_low_items()}")
    save_data()
    load_data()
    print_data()


if __name__ == "__main__":
    main()
