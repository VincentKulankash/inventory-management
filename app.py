from flask import Flask, jsonify, request
from inventory import inventory, get_next_id

app = Flask(__name__)

@app.route('/inventory', methods=['GET'])
def get_all_items():
    return jsonify(inventory), 200

@app.route('/inventory/<int:item_id>', methods=['GET'])
def get_one_item(item_id):
    item = next((i for i in inventory if i['id'] == item_id), None)
    if item is None:
        return jsonify({'error': f'Item {item_id} not found'}), 404

    return jsonify(item), 200

@app.route('/inventory', methods=['POST'])
def create_item():
    data = request.get_json(silent=True)

    if not data or not data.get('product_name'):
        return jsonify({'error':'product_name is required'}), 400

    new_item = {
        'id': get_next_id(),
        'product_name': data['product_name'],
        'brands': data.get('brands', ''),
        'ingredients_text': data.get('ingredients_text', ''),
        "price": float(data.get("price", 0.0)),
        'stock': int(data.get('stock', 0)),
    }

    inventory.append(new_item)
    return jsonify(new_item), 201
@app.route('/inventory/<int:item_id>', methods=['PATCH'])
def update_item(item_id):
    item = next((i for i in inventory if i['id'] == item_id), None)
    if item is None:
        return jsonify({'error':f'item {item_id} not found'}), 404

    data = request.get_json(silent=True) or {}
    allowed_fields = {'product_name', 'brands', 'ingredients_text', 'price', 'stock'}

    for field in allowed_fields:
        if field in data:
            if field == 'price':
                item[field] = float(data[field])
            elif field == 'stock':
                item[field] = int(data[field])
            else:
                item[field] = data[field]

    return jsonify(item), 200


@app.route('/inventory/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = next((i for i in inventory if i['id'] == item_id), None)
    if item is None:
        return jsonify({'error':f'item {item_id} not found'}), 404

    inventory.remove(item)
    return jsonify({'message':f'Item {item_id} deleted.'}), 200


if __name__ == "__main__":
    app.run(debug=True)
    

    