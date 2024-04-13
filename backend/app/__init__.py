import os

from flask import Flask
from flask_socketio import SocketIO
import redis
from app.routes import main as main_blueprint
import logging

def create_app():
    app = Flask(__name__, static_url_path='', static_folder='../../docs')
    app.config['REDIS_URL'] = os.getenv('REDIS_URL', 'redis://localhost:6379')
    app.redis = redis.Redis.from_url(app.config['REDIS_URL'])
    
    app.secret_key = os.getenv("FLASK_SECRET_KEY", "super_secret_key")
    
    logging.basicConfig(level=logging.DEBUG)
    app.logger.setLevel(logging.DEBUG)

    # Assuming the socketio setup is already imported and initialized in socketio_setup.py
    from app.socketio_setup import socketio
    socketio.init_app(app, cors_allowed_origins="https://seacelery.github.io")

    app.register_blueprint(main_blueprint)

    return app

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