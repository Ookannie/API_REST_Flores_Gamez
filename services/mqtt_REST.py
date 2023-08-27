# app.py
from flask import Blueprint, jsonify, request
from controls import control_mqtt as mqqt


control_mqtt = mqqt.ControlMQTT()
mqqt_bp = Blueprint("control_bp", __name__)

@mqqt_bp.route('/receive_ecg', methods=['POST'])
def receive_ecg():
    data = request.json
    ecg_value = data.get('ecg_value', None)
    if ecg_value:
        ecg_data = {"value": ecg_value, "timestamp": data.get('timestamp')}
        control_mqtt.create_ecg(ecg_data)
    return jsonify({"message": "Data received"}), 200

@mqqt_bp.route('/receive_alarm', methods=['POST'])
def receive_alarm():
    data = request.json
    alarm_message = data.get('alarm_message', None)
    if alarm_message:
        alarm_data = {"alarm": alarm_message, "timestamp": data.get('timestamp')}
        control_mqtt.create_alarm(alarm_data)
    return jsonify({"message": "Alarm received"}), 200


