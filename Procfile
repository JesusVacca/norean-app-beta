web: python manage.py collectstatic && gunicorn norean_app.wsgi:application --timeout 120 --workers 3 --bind 0.0.0.0:$PORT
