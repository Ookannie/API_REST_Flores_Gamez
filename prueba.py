from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

# Configuración de la base de datos MongoDB
mongo_client = MongoClient('mongodb://localhost:27017/')
db = mongo_client['electro']
users_collection = db['users']

# Definición del patrón DAO para los usuarios
class UserDAO:
    @staticmethod
    def get_all_users():
        return list(users_collection.find({}, {'_id': 0}))

    @staticmethod
    def get_user_by_id(user_id):
        return users_collection.find_one({'user_id': user_id}, {'_id': 0})

    @staticmethod
    def create_user(user_data):
        return users_collection.insert_one(user_data)

    @staticmethod
    def update_user(user_id, user_data):
        return users_collection.update_one({'user_id': user_id}, {'$set': user_data})

    @staticmethod
    def delete_user(user_id):
        return users_collection.delete_one({'user_id': user_id})


# Rutas de la API
@app.route('/users', methods=['GET'])
def get_users():
    users = UserDAO.get_all_users()
    return jsonify(users)

@app.route('/users/<string:user_id>', methods=['GET'])
def get_user(user_id):
    user = UserDAO.get_user_by_id(user_id)
    if user:
        return jsonify(user)
    else:
        return jsonify({'message': 'User not found'}), 404

@app.route('/users', methods=['POST'])
def create_user():
    user_data = request.json
    user_id = user_data.get('user_id')
    existing_user = UserDAO.get_user_by_id(user_id)
    if existing_user:
        return jsonify({'message': 'User already exists'}), 400

    result = UserDAO.create_user(user_data)
    return jsonify({'message': 'User created successfully', 'user_id': str(result.inserted_id)}), 201

@app.route('/users/<string:user_id>', methods=['PUT'])
def update_user(user_id):
    user_data = request.json
    result = UserDAO.update_user(user_id, user_data)
    if result.matched_count > 0:
        return jsonify({'message': 'User updated successfully'}), 200
    else:
        return jsonify({'message': 'User not found'}), 404

@app.route('/users/<string:user_id>', methods=['DELETE'])
def delete_user(user_id):
    result = UserDAO.delete_user(user_id)
    if result.deleted_count > 0:
        return jsonify({'message': 'User deleted successfully'}), 200
    else:
        return jsonify({'message': 'User not found'}), 404


if __name__ == '__main__':
    app.run(debug=True)
