from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.json_util import dumps
from bson.objectid import ObjectId

app = Flask(__name__)

# Folosim string-ul de conectare extras din db_create.py
CONNECTION_STRING = "mongodb+srv://alexandrucretu2611_db_user:Y6fJX13kSt3TTLsv@cluster0.drc7n4h.mongodb.net/?appName=Cluster0"
client = MongoClient(CONNECTION_STRING)

# Ne conectam la baza de date EventManagerDB si la colectia Evenimente
db = client["EventManagerDB"]
collection = db["Evenimente"]

@app.route('/entries', methods=['GET'])
def get_all_entries():
    """Returneaza toate evenimentele din baza de date."""
    entries = collection.find()
    return dumps(entries), 200

@app.route('/entries/<entry_id>', methods=['GET'])
def get_single_entry(entry_id):
    """Returneaza un singur eveniment din baza de date pe baza ID-ului."""
    try:
        # Cautam documentul convertind string-ul intr-un obiect ObjectId
        entry = collection.find_one({'_id': ObjectId(entry_id)})
        if entry:
            return dumps(entry), 200
        else:
            return jsonify({'error': 'Evenimentul nu a fost gasit'}), 404
    except Exception:
        return jsonify({'error': 'Formatul ID-ului este invalid'}), 400

@app.route('/entries', methods=['POST'])
def add_entry():
    """Adauga un nou eveniment in baza de date."""
    data = request.get_json()
    result = collection.insert_one(data)
    return jsonify({'_id': str(result.inserted_id)}), 201

@app.route('/entries/<entry_id>', methods=['PUT'])
def update_entry(entry_id):
    """Modifica un eveniment existent in baza de date."""
    try:
        data = request.get_json()
        # Folosim $set pentru a actualiza doar campurile trimise
        result = collection.update_one({'_id': ObjectId(entry_id)}, {'$set': data})
        
        if result.matched_count:
            return jsonify({'message': 'Evenimentul a fost actualizat cu succes'}), 200
        else:
            return jsonify({'error': 'Evenimentul nu a fost gasit pentru a fi actualizat'}), 404
    except Exception:
        return jsonify({'error': 'ID invalid sau format de date incorect'}), 400

@app.route('/entries/<entry_id>', methods=['DELETE'])
def delete_entry(entry_id):
    """Sterge un eveniment din baza de date pe baza ID-ului."""
    try:
        result = collection.delete_one({'_id': ObjectId(entry_id)})
        
        if result.deleted_count:
            return jsonify({'message': 'Evenimentul a fost sters cu succes'}), 200
        else:
            return jsonify({'error': 'Evenimentul nu a fost gasit pentru a fi sters'}), 404
    except Exception:
        return jsonify({'error': 'Formatul ID-ului este invalid'}), 400

if __name__ == '__main__':
    app.run(debug=True)