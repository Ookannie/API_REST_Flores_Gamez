# mqtt_publisher.py
import paho.mqtt.client as mqtt

# Configuración del broker MQTT
mqtt_broker = "10.178.10.147"
mqtt_port = 1883
mqtt_topic = "ecg/intervalo"

# Configuración y conexión del cliente MQTT
client = mqtt.Client()
client.connect(mqtt_broker, mqtt_port)

def publicar_intervalo(intervalo):
    client.publish(mqtt_topic, str(intervalo))
