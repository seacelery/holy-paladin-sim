web: gunicorn run:app
worker: celery -A app.celery worker -P solo --loglevel=info