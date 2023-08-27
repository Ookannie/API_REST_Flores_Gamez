from flask import Blueprint, jsonify, request
from controls import control_user as controlUser


control_user = controlUser.ControlUser()
user_bp = Blueprint("user_bp", __name__)


@user_bp.route('/users', methods=['GET'])
def get_users():
    users = control_user.get_all_users()
    return jsonify(users)

@user_bp.route('/users/<string:user_id>', methods=['GET'])
def get_user(user_id):
    user = control_user.get_user_by_id(user_id)
    if user:
        return jsonify(user)
    else:
        return jsonify({'message': 'User not found'}), 404

@user_bp.route('/users', methods=['POST'])
def create_user():
    user_data = request.json

    result = control_user.create_user(user_data)
    return jsonify({'message': 'User created successfully', 'user_id': str(result.inserted_id)}), 201

@user_bp.route('/users/<string:user_id>', methods=['PUT'])
def update_user(user_id):
    user_data = request.json
    result = control_user.update_user(user_id, user_data)
    if result.matched_count > 0:
        return jsonify({'message': 'User updated successfully'}), 200
    else:
        return jsonify({'message': 'User not found'}), 404

@user_bp.route('/users/<string:user_id>', methods=['DELETE'])
def delete_user(user_id):
    result = control_user.delete_user(user_id)
    if result.deleted_count > 0:
        return jsonify({'message': 'User deleted successfully'}), 200
    else:
        return jsonify({'message': 'User not found'}), 404