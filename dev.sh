python setup.py -q install
export APPINIT_DEVEL="true"

gunicorn appinit_auth.app.app:app -c appinit_auth/container/docker/auth/gunicorn.py
# webplatform-auth $@
