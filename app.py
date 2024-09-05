from flask import Flask, request, jsonify, abort
from datetime import datetime

app = Flask(__name__)

schedules = []

# Helper function to find a schedule by ID
def find_schedule(schedule_id):
    return next((schedule for schedule in schedules if schedule['id'] == schedule_id), None)

# GET /schedules - Get all schedules
@app.route('/schedules', methods=['GET'])
def get_schedules():
    return jsonify(schedules), 200

# GET /schedules/<int:id> - Get a specific schedule by ID
@app.route('/schedules/<int:schedule_id>', methods=['GET'])
def get_schedule(schedule_id):
    schedule = find_schedule(schedule_id)
    if schedule:
        return jsonify(schedule), 200
    else:
        return jsonify({'error': 'Schedule not found'}), 404
    
# POST /schedules - Create a new schedule
@app.route('/schedules', methods=['POST'])
def create_schedule():
    data = request.json  # Removed parentheses
    if 'name' not in data or 'start_time' not in data or 'end_time' not in data or 'staffId' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
    new_id = len(schedules) + 1
    schedule = {
        'id': new_id,
        'name': data['name'],
        'description': data.get('description', ''),
        'start_time': data['start_time'],
        'end_time': data['end_time'],
        'staffId': data['staffId'],
        'createdAt': datetime.now(),
        'updatedAt': datetime.now()
    }
    schedules.append(schedule)
    return jsonify(schedule), 201


# PUT /schedules/<int:id> - Update a schedule
@app.route('/schedules/<int:id>', methods=['PUT'])
def update_schedule(id):
    schedule = find_schedule(id)
    if schedule is None:
        return jsonify({'error': 'Schedule not found'}), 404
    
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    schedule['name'] = data.get('name', schedule['name'])
    schedule['description'] = data.get('description', schedule['description'])
    schedule['start_time'] = data.get('start_time', schedule['start_time'])
    schedule['end_time'] = data.get('end_time', schedule['end_time'])
    schedule['staffId'] = data.get('staffId', schedule['staffId'])
    schedule['updatedAt'] = datetime.now()
    return jsonify(schedule), 200

# DELETE /schedules/<int:id> - Delete a schedule
def delete_schedule(id):
    schedule = find_schedule(id)
    if schedule is None:
        return jsonify({'error': 'Schedule not found'}), 404
    schedules.remove(schedule)
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
     
