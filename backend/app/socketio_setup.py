from flask_socketio import SocketIO

socketio = SocketIO(cors_allowed_origins="*")

def init_socketio(app):
    redis_url = app.config["REDIS_TLS_URL"]
    socketio.init_app(app, async_mode='eventlet', logger=True, engineio_logger=True)