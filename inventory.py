"""Simulated data storage - an in memory array of inventory items"""

inventory = [
    {
        "id": 1,
        "product_name": "Organic Almond Milk",
        "brands": "Silk",
        "ingredients_text": "Filtered water, almonds, cane sugar",
        "price": 4.99,
        "stock": 25,
    },

    {
        "id": 2,
        "product_name": "Whole Wheat Bread",
        "brands": "Dave's Killer Bread",
        "ingredients_text": "Whole wheat flour, water, yeast, salt",
        "price": 5.49,
        "stock": 10,
    },
]

_next_id = 3  #next available id 1 and 2 are used 

def get_next_id():
    global _next_id
    new_id = _next_id
    _next_id += 1
    return new_id

"""In this we set the new id to next id then we increment next id so when adding a product next id gets set to 4. When deleting a product the next id remains the next available id but the id that was removed remains vacant not affecting our id however when you run len(inventory it will print something else)"""


