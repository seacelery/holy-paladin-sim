import os
from flask import Flask
import redis
import certifi
import pickle
from app.routes import main as main_blueprint
import logging
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from celery_config import make_celery

app = Flask(__name__, static_url_path="", static_folder="../../docs")
app.config["REDIS_TLS_URL"] = os.getenv("REDIS_TLS_URL")
app.redis = redis.Redis.from_url(
    app.config["REDIS_TLS_URL"],
    ssl_cert_reqs='none'
)

app.config.update(
    CELERY_BROKER_URL=app.config["REDIS_TLS_URL"] + '?ssl_cert_reqs=none',
    CELERY_RESULT_BACKEND=app.config["REDIS_TLS_URL"] + '?ssl_cert_reqs=none',
)

app.secret_key = os.getenv("FLASK_SECRET_KEY", "super_secret_key")

logging.basicConfig(level=logging.DEBUG)
app.logger.setLevel(logging.DEBUG)

CORS(app, supports_credentials=True, origins=["https://seacelery.github.io"], allow_headers=[
    "Content-Type", "Authorization", "X-Requested-With"], allow_methods=["GET", "POST", "OPTIONS"])

app.register_blueprint(main_blueprint)

# Initialize Celery
celery = make_celery(app)

def create_app():
    return app

def create_socketio(app):
    socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet", logger=True, engineio_logger=True)
    # register_socketio_events(socketio)
    return socketio

# def register_socketio_events(socketio):
#     @socketio.on('connect')
#     def handle_connect():
#         print('Client connected')

#     @socketio.on('disconnect')
#     def handle_disconnect():
#         print('Client disconnected')

#     @socketio.on('start_simulation')
#     def handle_start_simulation(data):
#         print("Received start_simulation data:", data)
#         emit('simple_response', {'message': 'Simple check complete'})

@celery.task
def process_paladin(paladin_data):
    # Deserialize the Paladin object
    paladin = pickle.loads(paladin_data)
    # Here you can add the code to process the Paladin object
    # For example, simulate or calculate results
    return paladin

# import os

# from flask import Flask
# from flask_cors import CORS
# from .socketio_setup import socketio
# from app.routes import main as main_blueprint

# flask_secret_key = os.getenv("FLASK_SECRET_KEY")

# import logging

# logging.basicConfig(level=logging.DEBUG)

# def create_app():
#     app = Flask(__name__, static_url_path='', static_folder='../../docs')
#     app.logger.setLevel(logging.DEBUG)
#     app.secret_key = flask_secret_key
#     CORS(app, supports_credentials=True)
#     app.register_blueprint(main_blueprint)
    
#     socketio.init_app(app)
#     return app