from flask_socketio import SocketIO

socketio = SocketIO(cors_allowed_origins="*")

def init_socketio(app):
    socketio.init_app(app, async_mode='eventlet', message_queue="rediss://:p07047fba795b7692e9c289c32b9129f04db91f5a51dadc7949bc932ea6d05bc0@ec2-34-250-232-88.eu-west-1.compute.amazonaws.com:10760", logger=True, engineio_logger=True)