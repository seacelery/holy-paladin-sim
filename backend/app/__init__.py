import os
import sys
import json
from flask import Flask, current_app
import redis
import certifi
import pickle
from app.routes import main as main_blueprint
from app.main import import_character
import logging
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from celery_config import make_celery

from app.classes.run_simulation_task import run_simulation_task

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
    register_socketio_events(socketio)
    return socketio

def register_socketio_events(socketio):
    @socketio.on('connect')
    def handle_connect():
        print('Client connected')

    @socketio.on('disconnect')
    def handle_disconnect():
        print('Client disconnected')

    @socketio.on('start_simulation')
    def handle_start_simulation(data):
        session_token = data.get('session_token')
        print(f"data received {session_token}")
        sys.stdout.flush()
        if not session_token:
            emit('error', {"error": "No session token provided"})
            return

        session_data = current_app.redis.get(session_token)
        if not session_data:
            emit('error', {"error": "Session not found"})
            return

        modifiable_data = json.loads(session_data)

        # Assuming import_character and other functions are accessible here
        paladin, healing_targets = import_character(
            modifiable_data['character_name'],
            modifiable_data['realm'],
            modifiable_data['region']
        )

        paladin.update_character(
            race=modifiable_data.get("race"),
            class_talents=modifiable_data.get("class_talents"),
            spec_talents=modifiable_data.get("spec_talents"),
            consumables=modifiable_data.get("consumables")
        )

        paladin_pickled = pickle.dumps(paladin)
        healing_targets_pickled = pickle.dumps(healing_targets)

        simulation_params = {
            "paladin": paladin_pickled,
            "healing_targets_list": healing_targets_pickled,
            "encounter_length": int(data['encounter_length']),
            "iterations": int(data['iterations']),
            "time_warp_time": int(data['time_warp_time']),
            "priority_list": data["priority_list"],
            "custom_equipment": data["custom_equipment"],
            "tick_rate": float(data['tick_rate']),
            "raid_health": int(data['raid_health']),
            "mastery_effectiveness": int(data['mastery_effectiveness']),
            "light_of_dawn_targets": int(data['light_of_dawn_targets']),
            "lights_hammer_targets": int(data['lights_hammer_targets']),
            "resplendent_light_targets": int(data['resplendent_light_targets']),
        }

        result = run_simulation_task.delay(simulation_parameters=simulation_params)
        emit('simulation_started', {'message': "Simulation started successfully, monitor progress via WebSocket.", 'task_id': str(result.id)})

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