from flask import Flask, jsonify, request
from datetime import datetime
import uuid

app = Flask(__name__)

# In-memory databases
users = {}
roles = {}
user_roles = []

# Helper Functions
def generate_id():
    return str(uuid.uuid4())

@app.route('/')
def home():
    return "Welcome to the User Provisioning System API!"

# Routes for Users
@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    if 'name' not in data or 'email' not in data:
        return jsonify({'error': 'Name and Email are required'}), 400
    if any(user['email'] == data['email'] for user in users.values()):
        return jsonify({'error': 'Email must be unique'}), 400
    user_id = generate_id()
    users[user_id] = {
        'id': user_id,
        'name': data['name'],
        'email': data['email'],
        'status': 'Active',
        'created_date': datetime.now().isoformat()
    }
    return jsonify(users[user_id]), 201

@app.route('/users', methods=['GET'])
def get_users():
    status_filter = request.args.get('status')
    filtered_users = [user for user in users.values() if not status_filter or user['status'] == status_filter]
    return jsonify(filtered_users), 200

@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = users.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user), 200

@app.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    user = users.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    data = request.json
    user['name'] = data.get('name', user['name'])
    user['status'] = data.get('status', user['status'])
    return jsonify(user), 200

@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = users.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    user['status'] = 'Inactive'
    return jsonify(user), 200

# Routes for Roles
@app.route('/roles', methods=['POST'])
def create_role():
    data = request.json
    if 'name' not in data:
        return jsonify({'error': 'Role name is required'}), 400
    role_id = generate_id()
    roles[role_id] = {
        'id': role_id,
        'name': data['name'],
        'description': data.get('description', '')
    }
    return jsonify(roles[role_id]), 201

@app.route('/roles', methods=['GET'])
def get_roles():
    return jsonify(list(roles.values())), 200

@app.route('/roles/<role_id>', methods=['GET'])
def get_role(role_id):
    role = roles.get(role_id)
    if not role:
        return jsonify({'error': 'Role not found'}), 404
    return jsonify(role), 200

@app.route('/roles/<role_id>', methods=['PUT'])
def update_role(role_id):
    role = roles.get(role_id)
    if not role:
        return jsonify({'error': 'Role not found'}), 404
    data = request.json
    role['name'] = data.get('name', role['name'])
    role['description'] = data.get('description', role['description'])
    return jsonify(role), 200

@app.route('/roles/<role_id>', methods=['DELETE'])
def delete_role(role_id):
    role = roles.pop(role_id, None)
    if not role:
        return jsonify({'error': 'Role not found'}), 404
    return jsonify({'message': 'Role deleted successfully'}), 200

# Routes for User Role Assignments
@app.route('/user-roles', methods=['POST'])
def assign_role():
    data = request.json
    if 'user_id' not in data or 'role_id' not in data:
        return jsonify({'error': 'User ID and Role ID are required'}), 400
    if data['user_id'] not in users or data['role_id'] not in roles:
        return jsonify({'error': 'Invalid User ID or Role ID'}), 400
    if any(assignment['user_id'] == data['user_id'] and assignment['role_id'] == data['role_id'] for assignment in user_roles):
        return jsonify({'error': 'Role already assigned to user'}), 400
    assignment_id = generate_id()
    user_roles.append({
        'id': assignment_id,
        'user_id': data['user_id'],
        'role_id': data['role_id'],
        'assigned_date': datetime.now().isoformat()
    })
    return jsonify({'id': assignment_id}), 201

@app.route('/user-roles', methods=['GET'])
def get_user_roles():
    user_id = request.args.get('user_id')
    role_id = request.args.get('role_id')
    filtered_roles = [assignment for assignment in user_roles if
                      (not user_id or assignment['user_id'] == user_id) and
                      (not role_id or assignment['role_id'] == role_id)]
    return jsonify(filtered_roles), 200

@app.route('/user-roles/<assignment_id>', methods=['DELETE'])
def delete_user_role(assignment_id):
    assignment = next((assignment for assignment in user_roles if assignment['id'] == assignment_id), None)
    if not assignment:
        return jsonify({'error': 'Assignment not found'}), 404
    user_roles.remove(assignment)
    return jsonify({'message': 'Assignment deleted successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)
