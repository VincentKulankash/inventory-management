# Inventory Management System

A Flask REST API with a CLI client for managing retail inventory, integrated with the [OpenFoodFacts](https://world.openfoodfacts.org/) API for real-time product data.

## Features

- Full CRUD on inventory items (GET / POST / PATCH / DELETE)
- Fetch product data from OpenFoodFacts by barcode or name
- Save fetched products directly into inventory
- 22 pytest tests (all mocked — no network required)

## Project Structure

```
inventory-management/
├── app.py              # Flask REST API routes
├── cli.py              # Terminal client
├── display.py          # Terminal formatting helpers
├── inventory.py        # In-memory storage
├── external_api.py     # OpenFoodFacts integration
├── tests/              # pytest suite
├── requirements.txt
└── README.md
```

## Installation

```bash
git clone https://github.com/VincentKulankash/inventory-management.git
cd inventory-management
python3 -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Running

Run the API and CLI in **two separate terminals**.

**Terminal 1 — API:**
```bash
python app.py
```

**Terminal 2 — CLI:**
```bash
python cli.py
```

## API Endpoints

Base URL: `http://127.0.0.1:5000`

| Method | Path | Description |
|---|---|---|
| GET | `/inventory` | List all items |
| GET | `/inventory/<id>` | Get one item |
| POST | `/inventory` | Add new item (`product_name` required) |
| PATCH | `/inventory/<id>` | Update item fields |
| DELETE | `/inventory/<id>` | Delete an item |
| GET | `/inventory/fetch/barcode/<barcode>` | Fetch product by barcode |
| GET | `/inventory/fetch/name/<name>` | Search products by name |

### Example Requests

```bash
curl http://127.0.0.1:5000/inventory

curl -X POST http://127.0.0.1:5000/inventory \
  -H "Content-Type: application/json" \
  -d '{"product_name": "Test Yogurt", "price": 1.99, "stock": 8}'

curl -X PATCH http://127.0.0.1:5000/inventory/1 \
  -H "Content-Type: application/json" -d '{"price": 9.99}'

curl -X DELETE http://127.0.0.1:5000/inventory/2

curl http://127.0.0.1:5000/inventory/fetch/barcode/3017620422003
```

## CLI Usage

The CLI presents a menu:

```
1. View all inventory
2. View a single item
3. Add a new item
4. Update an item
5. Delete an item
6. Fetch product from OpenFoodFacts (barcode)
7. Search OpenFoodFacts by name
0. Exit
```

**Example session:**
```
Choose an option: 1
ID | Name                | Brand | Price | Stock
---+---------------------+-------+-------+------
1  | Organic Almond Milk | Silk  | $4.99 | 25

Choose an option: 6
Barcode: 3017620422003
      product_name: Nutella
            brands: Ferrero
Save this item to inventory? (y/n): y
[OK] Saved as item id 3
```

## Testing

```bash
pytest -v
# 22 passed
```

## Tech Stack

Flask · requests · pytest · OpenFoodFacts API · in-memory storage

## Git Workflow

Features were developed on separate branches (`feature/crud-routes`, `feature/fetch-routes`, `feature/cli-interface`, `feature/tests`, `docs/readme`) and merged into `main` via pull requests.

## Author

Vincent Kulankash — vincent.kulankash@student.moringaschool.com