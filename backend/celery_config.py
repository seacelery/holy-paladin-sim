from celery import Celery

def make_celery(app):
    broker_url = app.config['CELERY_BROKER_URL']
    backend_url = app.config['CELERY_RESULT_BACKEND']

    celery = Celery(app.import_name, broker=broker_url, backend=backend_url)
    
    celery.conf.update(
        accept_content=['pickle', 'json'],
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