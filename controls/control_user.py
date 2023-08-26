from DAOS import user_DAO

class ControlUser:

    def __init__ (self):
        self.userDAO = user_DAO.UserDAO()

    def get_all_users(self):
        return self.userDAO.get_all_users()

    
    def get_user_by_id(self, user_id):
        return self.userDAO.get_user_by_id(user_id)

    
    def create_user(self, user_data):
        return self.userDAO.create_user(user_data)

    
    def update_user(self, user_id, user_data):
        return self.userDAO.update_user(user_id, user_data)

    
    def delete_user(self, user_id):
        return self.userDAO.delete_user({'user_id': user_id})