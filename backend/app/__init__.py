import os
from flask import Flask, session
from flask_cors import CORS
import redis
from .socketio_setup import socketio
from app.routes import main as main_blueprint
import logging

def create_app():
    app = Flask(__name__, static_url_path='', static_folder='../../docs')
    app.secret_key = os.getenv("FLASK_SECRET_KEY", "default_secret_key")
    app.config['SESSION_REDIS'] = redis.from_url(os.environ.get('REDIS_URL', 'redis://localhost:6379'))
    
    app.logger.setLevel(logging.DEBUG)
    CORS(app, supports_credentials=True)
    app.register_blueprint(main_blueprint)
    
    socketio.init_app(app)

    return app