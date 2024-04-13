import os
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
import redis
from app.routes import main as main_blueprint
import logging

def create_app():
    app = Flask(__name__, static_url_path='', static_folder='../../docs')
    app.config['REDIS_URL'] = os.getenv('REDIS_URL', 'redis://localhost:6379')
    app.redis = redis.Redis.from_url(app.config['REDIS_URL'])
    
    app.secret_key = os.getenv("FLASK_SECRET_KEY", "default_secret_key")
    logging.basicConfig(level=logging.DEBUG)
    app.logger.setLevel(logging.DEBUG)
    
    CORS(app, supports_credentials=True)
    app.register_blueprint(main_blueprint)
    
    socketio = SocketIO(app)
    socketio.init_app(app)
    
    return app