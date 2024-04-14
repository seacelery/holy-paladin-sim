import os
from flask import Flask
import redis
from app.routes import main as main_blueprint
import logging
from flask_cors import CORS
from flask_socketio import SocketIO
from celery_config import make_celery  # Assuming celery_config.py is in the same directory

app = Flask(__name__, static_url_path="", static_folder="../../docs")
app.config["REDIS_URL"] = os.getenv("REDIS_URL", "redis://localhost:6379")
app.config.update(
    CELERY_BROKER_URL=os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0'),
    CELERY_RESULT_BACKEND=os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
)
app.redis = redis.Redis.from_url(app.config["REDIS_URL"])
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
    socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")
    return socketio

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