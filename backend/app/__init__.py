import os

from flask import Flask
from flask_cors import CORS
from .socketio_setup import socketio
from app.routes import main as main_blueprint

flask_secret_key = os.getenv("FLASK_SECRET_KEY")

def create_app():
    app = Flask(__name__, static_url_path='', static_folder='../../docs')
    app.secret_key = flask_secret_key
    CORS(app, supports_credentials=True)
    app.register_blueprint(main_blueprint)
    
    socketio.init_app(app)
    return app