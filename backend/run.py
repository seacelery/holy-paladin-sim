import os
import sys
from dotenv import load_dotenv
load_dotenv()

from app import create_app, socketio, celery
print("Initializing Celery in run:", celery)
print(celery.conf)
sys.stdout.flush()

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host='0.0.0.0', port=port)