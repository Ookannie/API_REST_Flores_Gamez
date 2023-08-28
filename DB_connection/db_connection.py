from pymongo import MongoClient

'''
Archivo encargado de inicializar la conexión a la base de datos con Mango
'''

mongo_client = MongoClient('mongodb://localhost:27017/')
db = mongo_client['electro']

 