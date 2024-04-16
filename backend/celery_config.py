from celery import Celery
import os
import pickle

def make_celery(app):
    # Get broker and backend URLs from the Flask app config
    broker_url = app.config['CELERY_BROKER_URL']
    backend_url = app.config['CELERY_RESULT_BACKEND']

    # Create the Celery app instance with broker and backend
    celery = Celery(app.import_name, broker=broker_url, backend=backend_url)
    
    # Celery configuration to use pickle as the serializer
    celery.conf.update(
        accept_content=['pickle', 'json'],  # Allows accepting both pickle and json.
        task_serializer='pickle',
        result_serializer='pickle',
        enable_utc=True,
        timezone='UTC',
        broker_connection_retry_on_startup=True
    )
    
    celery.conf.result_expires = 120

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery