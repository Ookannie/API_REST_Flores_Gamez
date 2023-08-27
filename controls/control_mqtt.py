from DAOS import mqtt_DAO

class ControlMQTT:

    def __init__ (self):
        self.mqttDAO = mqtt_DAO.MQTT_DAO()


    
    def create_ecg(self, ecg_data):
        return self.mqttDAO.create_ecg(ecg_data)
    
    def create_alarm(self, alarm_data):
        return self.mqttDAO.create_alarm(alarm_data)

    