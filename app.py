from flask import Flask, request, jsonify
from pymongo import MongoClient
from pydantic import BaseModel

app = Flask(__name__)
client = MongoClient("mongodb://admin:14072002@localhost:27017/admin")
db = client["bancodados"]
collection = db["items"]

class Item(BaseModel):
    name: str
    description: str

@app.route('/api/items', methods=['GET'])
def get_all_items():
    items = list(collection.find())
    return jsonify(items)

@app.route('/api/items/<item_id>', methods=['GET'])
def get_item(item_id):
    item = collection.find_one({"_id": item_id})
    if item:
        return jsonify(item)
    else:
        return jsonify({"message": "Item não encontrado"}), 404

@app.route('/api/items', methods=['POST'])
def create_item():
    data = request.get_json()
    item = Item(**data)
    inserted_item = collection.insert_one(item.dict())
    return jsonify({"message": "Item criado com sucesso", "item_id": str(inserted_item.inserted_id)})

if __name__ == '__main__':
    app.run(debug=True)
