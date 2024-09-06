from flask import Flask, request, jsonify, abort
from datetime import datetime
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient("mongodb+srv://unwanaudo:L3tM3In@on-call-cluster.um0iw.mongodb.net/on-call-scheduler?retryWrites=true&w=majority&ssl=true")

db = client["on-call-scheduler"]

schedules_collection = db["schedules"]

# Helper function to find a schedule by ID
def find_schedule(schedule_id):
    return next((schedule for schedule in schedules if schedule['id'] == schedule_id), None)

# GET /schedules - Get all schedules
@app.route('/schedules', methods=['GET'])
def get_schedules():
    schedules = list(schedules_collection.find())
    for schedule in schedules:
        schedule['_id'] = str(schedule['_id'])
    return jsonify(schedules), 200

# GET /schedules/<int:id> - Get a specific schedule by ID
@app.route('/schedules/<int:schedule_id>', methods=['GET'])
def get_schedule(schedule_id):
    try:
        schedule = schedules_collection.find_one({'_id': ObjectId(schedule_id)})
        if not schedule:
            return jsonify({'error': 'Schedule not found'}), 404
        schedule['_id'] = str(schedule['_id'])
        return jsonify(schedule), 200
    except:
        return jsonify({'error': 'Invalid ID'}), 400
    
# POST /schedules - Create a new schedule
@app.route('/schedules', methods=['POST'])
def create_schedule():
    data = request.json
    if 'name' not in data or 'start_time' not in data or 'end_time' not in data or 'staffId' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Check if the schedule already exists (based on name, start_time, and staffId)
    existing_schedule = schedules_collection.find_one({
        'name': data['name'],
        'start_time': data['start_time'],
        'staffId': data['staffId']
    })
    
    if existing_schedule:
        return jsonify({'error': 'Duplicate schedule'}), 409  # 409 Conflict

    schedule = {
        'name': data['name'],
        'description': data.get('description', ''),
        'start_time': data['start_time'],
        'end_time': data['end_time'],
        'staffId': data['staffId'],
        'createdAt': datetime.now(),
        'updatedAt': datetime.now()
    }
    result = schedules_collection.insert_one(schedule)
    schedule['_id'] = str(result.inserted_id)
    return jsonify(schedule), 201



# PUT /schedules/<int:id> - Update a schedule
@app.route('/schedules/<string:schedule_id>', methods=['PUT'])
def update_schedule(schedule_id):
    schedule = schedules_collection.find_one({"_id": ObjectId(schedule_id)})
    if schedule is None:
        return jsonify({'error': 'Schedule not found'}), 404
    
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    updated_schedule = {
        'name': data.get('name', schedule['name']),
        'description': data.get('description', schedule['description']),
        'start_time': data.get('start_time', schedule['start_time']),
        'end_time': data.get('end_time', schedule['end_time']),
        'staffId': data.get('staffId', schedule['staffId']),
        'updatedAt': datetime.now()
    }
    
    schedules_collection.update_one({"_id": ObjectId(schedule_id)}, {"$set": updated_schedule})
    
    updated_schedule['_id'] = str(schedule['_id'])  # Ensure _id is converted to string
    
    return jsonify(updated_schedule), 200


# DELETE /schedules/<int:id> - Delete a schedule
@app.route('/schedules/<schedule_id>', methods=['DELETE'])
def delete_schedule(schedule_id):
    try:
        result = schedules_collection.delete_one({'_id': ObjectId(schedule_id)})
        if result.deleted_count == 0:
            return jsonify({'error': 'Schedule not found'}), 404
        return '', 204
    except Exception:
        return jsonify({'error': 'Invalid ID format'}), 400


if __name__ == '__main__':
    app.run(debug=True)
     
