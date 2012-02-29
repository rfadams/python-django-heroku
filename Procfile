web: python web/manage.py collectstatic --noinput; gunicorn_django --workers=4 --bind=0.0.0.0:$PORT web/settings.py
