from DB_connection import db_connection

class MQTT_DAO:
    '''
    Clase que implementa el patrón de diseño Data access 
    object para la lógica de base de datos de la colección ecg_signals
    '''
    def __init__(self):
        self.ECG_collection = db_connection.db['ecg_data']
        self.alarms_collection = db_connection.db['alarms']

    

    def create_ecg(self, ecg_data):
        return self.ECG_collection.insert_one(ecg_data)
    
    def create_alarm(self, ecg_data):
        return self.alarms_collection.insert_one(ecg_data)
