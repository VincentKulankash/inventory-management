import requests

BASE_URL = 'https://world.openfoodfacts.org'
HEADERS = {'User-Agent': 'Inventory-Management-Lab/1.0 (vincent.kulankash@student.moringaschool.com)'}


def fetch_by_barcode(barcode: str):
    """Fetch a product by a barcode that returns a dict or none """
    url = f"{BASE_URL}/api/v2/product/{barcode}.json"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        resp.raise_for_status() #raise_for_status() function lets the request blow up now instead of using the bad response
        data = resp.json()
        if data.get('status') == 1 or 'product' in data:
            return data['product']
        return None
    
    #requests.RequestsException as e catches all errors that might arise from our try block be it timeout error, HTTP error or any other error 
    except requests.RequestException as e:
        print(f"[API ERROR] {e}")
        return None

def fetch_by_name(name: str):
    #Fetch a product by its name. Return a list of product dicts
    url = f"{BASE_URL}/cgi/search.pl"
    params = {"search_terms": name, 'search_simple': 1, "json": 1}
    try:
        resp = requests.get(url, params=params, headers=HEADERS, timeout= 15)
        resp.raise_for_status()
        data = resp.json()
        return data.get('products', [])
    except requests.RequestException as e:
        print(f"[API ERROR] {e}")
        return []

def extract_fields(product: dict) -> dict:
    #Pull the fields we care about from a raw OpenFoodFacts product.
    return {
        'product_name' : product.get('product_name', 'Unknown'),
        'brands' : product.get('brands', 'Unknown'),
        'ingredients_text' : product.get('ingredients_text', ''),
    }



    