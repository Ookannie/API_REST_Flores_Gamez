import unittest
from prueba import app, UserDAO

class TestUserAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        # Insertamos algunos usuarios para las pruebas
        user_data_1 = {
            'user_id': 'user001',
            'name': 'John Doe',
            'age': 30,
            'email': 'john@example.com',
            'thresholds': [
                {'name': 'Temperature', 'high': 100, 'low': 0},
                {'name': 'Humidity', 'high': 80, 'low': 20},
            ],
        }
        user_data_2 = {
            'user_id': 'user002',
            'name': 'Jane Smith',
            'age': 25,
            'email': 'jane@example.com',
            'thresholds': [
                {'name': 'Temperature', 'high': 95, 'low': 5},
                {'name': 'Humidity', 'high': 75, 'low': 25},
            ],
        }
        UserDAO.create_user(user_data_1)
        UserDAO.create_user(user_data_2)

    def tearDown(self):
        # Eliminamos los usuarios creados durante las pruebas
        UserDAO.delete_user('user001')
        UserDAO.delete_user('user002')

    def test_get_all_users(self):
        response = self.app.get('/users')
        data = response.json
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 2)

    def test_get_user_by_id(self):
        response = self.app.get('/users/user001')
        data = response.json
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['user_id'], 'user001')
        self.assertEqual(data['name'], 'John Doe')

    def test_get_user_by_invalid_id(self):
        response = self.app.get('/users/nonexistent_user')
        self.assertEqual(response.status_code, 404)

    def test_create_user(self):
        new_user_data = {
            'user_id': 'user003',
            'name': 'New User',
            'age': 28,
            'email': 'newuser@example.com',
            'thresholds': [
                {'name': 'Temperature', 'high': 90, 'low': 10},
                {'name': 'Humidity', 'high': 70, 'low': 30},
            ],
        }
        response = self.app.post('/users', json=new_user_data)
        data = response.json
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['message'], 'User created successfully')
        self.assertIsNotNone(data['user_id'])

    def test_create_duplicate_user(self):
        existing_user_data = {
            'user_id': 'user001',
            'name': 'Duplicate User',
            'age': 25,
            'email': 'duplicate@example.com',
            'thresholds': [],
        }
        response = self.app.post('/users', json=existing_user_data)
        data = response.json
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], 'User already exists')

    def test_update_user(self):
        updated_user_data = {
            'name': 'Updated User',
            'email': 'updated@example.com',
            'age': 32,
            'thresholds': [
                {'name': 'Temperature', 'high': 110, 'low': 10},
            ],
        }
        response = self.app.put('/users/user001', json=updated_user_data)
        data = response.json
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], 'User updated successfully')

        # Verificar que los cambios se han aplicado
        response = self.app.get('/users/user001')
        data = response.json
        self.assertEqual(data['name'], 'Updated User')
        self.assertEqual(data['email'], 'updated@example.com')
        self.assertEqual(data['age'], 32)
        self.assertEqual(len(data['thresholds']), 1)

    def test_update_nonexistent_user(self):
        response = self.app.put('/users/nonexistent_user', json={})
        self.assertEqual(response.status_code, 404)

    def test_delete_user(self):
        response = self.app.delete('/users/user002')
        data = response.json
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], 'User deleted successfully')

        # Verificar que el usuario ha sido eliminado
        response = self.app.get('/users/user002')
        self.assertEqual(response.status_code, 404)

    def test_delete_nonexistent_user(self):
        response = self.app.delete('/users/nonexistent_user')
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
