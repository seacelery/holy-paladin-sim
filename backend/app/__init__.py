from flask import Flask
from flask_cors import CORS
from .socketio_setup import socketio
from app.routes import main as main_blueprint

def create_app():
    app = Flask(__name__)
    app.secret_key = 'dhjwa36yuajwdoa29d8djaiwdjia82djawd82auaj'
    CORS(app, supports_credentials=True)
    app.register_blueprint(main_blueprint)
    
    socketio.init_app(app)
    return app