import asyncio
import websockets
from flask import Blueprint, jsonify, request
from controls import control_mqtt as mqqt
import threading
import queue
import json
from bson import ObjectId
#from mqtt_publicador import publicar_intervalo

#Blueprint para el servicio REST para la lógica de las peticiones de MQTT

control_mqtt = mqqt.ControlMQTT()
mqtt_bp = Blueprint("mqtt_bp", __name__)

data_queue = queue.Queue()
websocket = None  

async def send_data(data):
    global websocket
    if websocket is None or websocket.closed:
        websocket = await websockets.connect("ws://127.0.0.1:8000/ws/ecg/")
        print(data)
    json_data = json.dumps(data, cls=JSONEncoder)  # Use the custom encoder here
    await websocket.send(json_data)


def websocket_thread():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    global websocket
    try:
        while True:
            data = data_queue.get()
            if data == "exit":
                break
            loop.run_until_complete(send_data(data))
    except Exception as e:
        print(f"WebSocket Error: {e}")
        websocket = None  
    finally:
        loop.run_until_complete(websocket.close())
        loop.close()

@mqtt_bp.route('/receive_ecg', methods=['POST'])
def receive_ecg():
    data = request.json
    ecg_value = data.get('ecg_value', None)
    if ecg_value:
        ecg_data = {"value": ecg_value, "timestamp": data.get('timestamp')}
        control_mqtt.create_ecg(ecg_data)
        data_queue.put(ecg_data)
    return jsonify({"message": "Data received"}), 200

@mqtt_bp.route('/receive_alarm', methods=['POST'])
def receive_alarm():
    data = request.json
    alarm_message = data.get('alarm_message', None)
    if alarm_message:
        alarm_data = {"alarm": alarm_message, "timestamp": data.get('timestamp')}
        control_mqtt.create_alarm(alarm_data)
        data_queue.put(alarm_data)
    return jsonify({"message": "Alarm received"}), 200

@mqtt_bp.route('/receive_alarm_taquicardia', methods=['POST'])
def receive_alarm_taquicardia():
    data = request.json
    alarm_message = data.get('alarm_message', None)
    if alarm_message:
        alarm_data = {"alarm": alarm_message, "type": "Taquicardia", "timestamp": data.get('timestamp')}
        control_mqtt.create_alarm(alarm_data)
        data_queue.put(alarm_data)
    return jsonify({"message": "Alarm received"}), 200

@mqtt_bp.route('/receive_alarm_bradicardia', methods=['POST'])
def receive_alarm_bradicardia():
    data = request.json
    alarm_message = data.get('alarm_message', None)
    if alarm_message:
        alarm_data = {"alarm": alarm_message, "type": "Bradicardia", "timestamp": data.get('timestamp')}
        control_mqtt.create_alarm(alarm_data)
        data_queue.put(alarm_data)
    return jsonify({"message": "Alarm received"}), 200

@mqtt_bp.route('/actualizar_intervalo', methods=['POST'])
def actualizar_intervalo():
    intervalo = request.form.get('intervalo')
    if intervalo:
        try:
           
            #intervalo = int(intervalo)
           # publicar_intervalo(intervalo)
            return jsonify({"message": "Interval updated successfully"}), 200
        except ValueError:
            return jsonify({"error": "Invalid interval value"}), 400
    else:
        return jsonify({"error": "No interval provided"}), 400


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return super().default(o)




thread = threading.Thread(target=websocket_thread)
thread.start()
