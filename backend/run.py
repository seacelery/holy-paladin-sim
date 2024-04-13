import os
from dotenv import load_dotenv
load_dotenv()

from app import create_app, create_socketio

app = create_app()
socketio = create_socketio(app)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    # Here we run the SocketIO with eventlet, but only use eventlet's monkey patching here
    socketio.run(app, host='0.0.0.0', port=port)