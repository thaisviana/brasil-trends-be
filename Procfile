web: gunicorn trendsApi.wsgi
celery: celery worker --beat -A trendsApi.celery_app --loglevel=info