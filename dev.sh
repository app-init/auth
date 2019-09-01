export APPINIT_DEVEL="true"

gunicorn appinit_auth.app.app:app -c gunicorn.py
