import sys
import requests

from display import print_table, print_item, success, error
BASE_URL = 'http://127.0.0.1:5000'

#Menu actions
def view_all():
    try:
        r = requests.get(f"{BASE_URL}/inventory", timeout=5)
        r.raise_for_status()
        print_table(r.json())
    except requests.RequestException as e:
        error(f"Could not reach the API: {e}")

def view_one():
    item_id = input('Item ID: ').strip()
    try:
        r = requests.get(f"{BASE_URL}/inventory/{item_id}", timeout=5)
        if r.status_code == 200:
            print_item(r.json())
        else:
            error(r.json().get('error', 'Item not found'))
    except requests.RequestException as e:
        error(f"Could not reach the API: {e}")

def add_item():
    name = input('Product name: ').strip()
    if not name:
        error('Product name is required')
        return

    brand = input("Brand: ").strip()
    ingredients = input("Ingredients: ").strip()
    price_raw = input("Price (default 0): ").strip() or "0"
    stock_raw = input("Stock (default 0): ").strip() or "0"

    try:
        price = float(price_raw)
        stock = int(stock_raw)
    except ValueError:
        error('Price must be a number and stock must be an integer')
        return

    payload = {
        "product_name": name,
        "brands": brand,
        "ingredients_text": ingredients,
        "price": price,
        "stock": stock,
    }

    try:
        r = requests.post(f"{BASE_URL}/inventory", json=payload, timeout=5)
        if r.status_code == 201:
            success(f"Added item with id {r.json()['id']}")
        else:
            error(r.json().get('error', 'Failed to add item'))

    except requests.RequestException as e:
        error(f"Could not reach the API: {e}")

def update_item():
    item_id = input("Item ID to update: ").strip()
    field = input("Field to update (product_name/brands/ingredients_text/price/stock): ").strip()
    value = input("New value: ").strip()

    allowed = {"product_name", "brands", "ingredients_text", "price", "stock"}
    if field not in allowed:
        error(f"Invalid field. Allowed: {', '.join(sorted(allowed))}")
        return

    # Cast numeric fields
    try:
        if field == "price":
            value = float(value)
        elif field == "stock":
            value = int(value)
    except ValueError:
        error(f"'{field}' must be numeric.")
        return

    try:
        r = requests.patch(f"{BASE_URL}/inventory/{item_id}", json={field: value}, timeout=5)
        if r.status_code == 200:
            success(f"Updated item {item_id}")
            print_item(r.json())
        else:
            error(r.json().get("error", "Failed to update item"))
    except requests.RequestException as e:
        error(f"Could not reach the API: {e}")

def delete_item():
    item_id = input("Item ID to delete: ").strip()
    try:
        r = requests.delete(f"{BASE_URL}/inventory/{item_id}", timeout=5)
        if r.status_code == 200:
            success(f"Deleted item {item_id}")
        else:
            error(r.json().get("error", "Failed to delete item"))
    except requests.RequestException as e:
        error(f"Could not reach the API: {e}")

def fetch_barcode():
    barcode = input("Barcode: ").strip()
    try:
        r = requests.get(f"{BASE_URL}/inventory/fetch/barcode/{barcode}", timeout=20)
        if r.status_code == 200:
            product = r.json()
            print_item(product)

            save = input("Save this item to inventory? (y/n): ").strip().lower()
            if save == "y":
                payload = {
                    "product_name": product.get("product_name", ""),
                    "brands": product.get("brands", ""),
                    "ingredients_text": product.get("ingredients_text", ""),
                    "price": 0.0,
                    "stock": 0,
                }
                post = requests.post(f"{BASE_URL}/inventory", json=payload, timeout=5)
                if post.status_code == 201:
                    success(f"Saved as item id {post.json()['id']}")
                else:
                    error(post.json().get("error", "Failed to save"))
        else:
            error(r.json().get("error", "Product not found"))
    except requests.RequestException as e:
        error(f"Could not reach the API: {e}")

def fetch_name():
    name = input("Product name to search: ").strip()
    try:
        r = requests.get(f"{BASE_URL}/inventory/fetch/name/{name}", timeout=20)
        if r.status_code == 200:
            products = r.json()
            # Add placeholder id/price/stock so print_table works
            display_rows = [
                {**p, "id": "-", "price": 0, "stock": 0} for p in products
            ]
            print_table(display_rows)
        else:
            error(r.json().get("error", "No products found"))
    except requests.RequestException as e:
        error(f"Could not reach the API: {e}")


#Menu loop 

def print_menu():
    print("""
INVENTORY MANAGEMENT
1. View all inventory
2. View a single item
3. Add a new item 
4. Update an item 
5. Delete an item 
6. Fetch product from OpenFoodFacts (Barcode)
7. Search OpenFoodFacts by name
0. Exit 
""")


def main():
    actions = {
        '1': view_all,
        '2': view_one,
        '3': add_item,
        '4': update_item,
        '5': delete_item,
        '6': fetch_barcode,
        '7': fetch_name,
    }

    while True:
        print_menu()
        choice = input('Choose an option: ').strip()

        if choice == '0':
            print('Goodbye.')
            sys.exit(0)

        action = actions.get(choice)
        if action is None:
            error('Invalid choice.')
            continue

        try:
            action()
        except KeyboardInterrupt:
            print('\nInterrupted. Back to Menu.')
        except Exception as e:
            error(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()

    