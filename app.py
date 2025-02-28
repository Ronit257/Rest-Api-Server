from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson.objectid import ObjectId
import json

app = Flask(__name__)
CORS(app)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['media_database']
collection = db['media_items']

# Initialize the database with sample data if empty
if collection.count_documents({}) == 0:
    sample_data = [
        {
            "name": "Harry Potter and the Order of the Phoenix",
            "img": "https://bit.ly/2IcnSwz",
            "summary": "Harry Potter and Dumbledore's warning about the return of Lord Voldemort is not heeded by the wizard authorities who, in turn, look to undermine Dumbledore's authority at Hogwarts and discredit Harry."
        },
        {
            "name": "The Lord of the Rings: The Fellowship of the Ring",
            "img": "https://bit.ly/2tC1Lcg",
            "summary": "A young hobbit, Frodo, who has found the One Ring that belongs to the Dark Lord Sauron, begins his journey with eight companions to Mount Doom, the only place where it can be destroyed."
        },
        {
            "name": "Avengers: Endgame",
            "img": "https://bit.ly/2Pzczlb",
            "summary": "Adrift in space with no food or water, Tony Stark sends a message to Pepper Potts as his oxygen supply starts to dwindle. Meanwhile, the remaining Avengers -- Thor, Black Widow, Captain America, and Bruce Banner -- must figure out a way to bring back their vanquished allies for an epic showdown with Thanos -- the evil demigod who decimated the planet and the universe."
        }
    ]
    collection.insert_many(sample_data)

# Helper function to convert ObjectId to string
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return super().default(o)

# Create - POST endpoint
@app.route('/api/media', methods=['POST'])
def create_media():
    data = request.json
    if not data or not 'name' in data or not 'img' in data or not 'summary' in data:
        return jsonify({"error": "Missing required fields"}), 400
    
    media_id = collection.insert_one(data).inserted_id
    return jsonify({"message": "Media added successfully", "id": str(media_id)}), 201

# Read all - GET endpoint
@app.route('/api/media', methods=['GET'])
def get_all_media():
    media_items = list(collection.find())
    return JSONEncoder().encode(media_items), 200, {'Content-Type': 'application/json'}

# Read one - GET endpoint
@app.route('/api/media/<id>', methods=['GET'])
def get_media(id):
    try:
        media = collection.find_one({"_id": ObjectId(id)})
        if media:
            return JSONEncoder().encode(media), 200, {'Content-Type': 'application/json'}
        return jsonify({"error": "Media not found"}), 404
    except:
        return jsonify({"error": "Invalid ID format"}), 400

# Update - PUT endpoint
@app.route('/api/media/<id>', methods=['PUT'])
def update_media(id):
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400

        result = collection.update_one({"_id": ObjectId(id)}, {"$set": data})
        if result.matched_count:
            return jsonify({"message": "Media updated successfully"}), 200
        return jsonify({"error": "Media not found"}), 404
    except:
        return jsonify({"error": "Invalid ID format"}), 400

# Delete - DELETE endpoint
@app.route('/api/media/<id>', methods=['DELETE'])
def delete_media(id):
    try:
        result = collection.delete_one({"_id": ObjectId(id)})
        if result.deleted_count:
            return jsonify({"message": "Media deleted successfully"}), 200
        return jsonify({"error": "Media not found"}), 404
    except:
        return jsonify({"error": "Invalid ID format"}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)