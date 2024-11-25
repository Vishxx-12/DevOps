from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["TreasureBookDB"]

@app.route('/node', methods=['POST'])
def add_node():
    data = request.json
    node_type = data.get("Type")
    node_data = data.get("Data")
    
    if not node_type or not node_data:
        return jsonify({"error": "Type and Data are required"}), 400
    
    # Insert the node into the appropriate collection
    collection = db[node_type]
    node_id = collection.insert_one(node_data).inserted_id
    
    return jsonify({"message": "Node added", "node_id": str(node_id)}), 201

@app.route('/edge', methods=['POST'])
def add_edge():
    data = request.json
    edge_type = data.get("Type")
    source = data.get("Source")
    target = data.get("Target")
    
    if not edge_type or not source or not target:
        return jsonify({"error": "Type, Source, and Target are required"}), 400
    
    # Insert the edge into the 'Edges' collection
    edge = {"Type": edge_type, "Source": source, "Target": target}
    edge_id = db["Edges"].insert_one(edge).inserted_id
    
    return jsonify({"message": "Edge added", "edge_id": str(edge_id)}), 201

@app.route('/status', methods=['GET'])
def status():
    return jsonify({"message": "TreasureBook API is running"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
