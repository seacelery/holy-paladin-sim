from flask import Flask
from flask_cors import CORS
from .socketio_setup import socketio
from app.routes import main as main_blueprint
from app.classes.config import FLASK_SECRET_KEY

def create_app():
    app = Flask(__name__)
    app.secret_key = FLASK_SECRET_KEY
    CORS(app, supports_credentials=True)
    app.register_blueprint(main_blueprint)
    
    socketio.init_app(app)
    return app