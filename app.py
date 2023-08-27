from flask import Flask
from services import user_REST, mqtt_REST

app = Flask(__name__)

app.register_blueprint(user_REST.user_bp)
app.register_blueprint(mqtt_REST.mqqt_bp)

if __name__ == "__main__":
    app.run(debug=True)
