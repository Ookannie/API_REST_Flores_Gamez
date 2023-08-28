from flask import Flask
from services import user_REST, mqtt_REST
from flask_socketio import SocketIO

'''
Archivo encargado de inicializar la aplicación Flask y el websocket
'''

app = Flask(__name__)
socketio = SocketIO(app) 

@app.route('/')
def index():
    return "Hello, World!"

if __name__ == "__main__":
    try:
        app.register_blueprint(user_REST.user_bp)
        app.register_blueprint(mqtt_REST.mqtt_bp)
        socketio.run(app, debug=True, host='127.0.0.1', port=5000)
    finally:
       
        mqtt_REST.data_queue.put("exit")
        mqtt_REST.thread.join()
