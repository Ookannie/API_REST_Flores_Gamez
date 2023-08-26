from DB_connection import db_connection

class UserDAO:

    def __init__(self):
        self.users_collection = db_connection.db['users']

    
    def get_all_users(self):
        return list(self.users_collection.find({}, {'_id': 0}))

    
    def get_user_by_id(self, user_id):
        return self.users_collection.find_one({'user_id': user_id}, {'_id': 0})

    
    def create_user(self, user_data):
        return self.users_collection.insert_one(user_data)

    
    def update_user(self, user_id, user_data):
        return self.users_collection.update_one({'user_id': user_id}, {'$set': user_data})

    
    def delete_user(self, user_id):
        return self.users_collection.delete_one({'user_id': user_id})