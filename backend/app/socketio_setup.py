from flask_socketio import SocketIO

socketio = SocketIO(cors_allowed_origins="*")

def init_socketio(app):
    socketio.init_app(app, async_mode='eventlet', logger=True, engineio_logger=True)