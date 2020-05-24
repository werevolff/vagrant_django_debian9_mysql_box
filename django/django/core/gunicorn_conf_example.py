import environ
import os

env = environ.Env(
    BACKEND_RELOAD_MODE=(bool, True),
    GUNICORN_BACKEND_LOG_DIR=(str, ''),
    GUNICORN_BACKEND_PID_DIR=(str, ''),
    DEFAULT_USER=(str, ''),
)

ROOT = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)
environ.Env.read_env(os.path.join(ROOT, '.env'))

reload = env('BACKEND_RELOAD_MODE')

pid = os.path.join(env('GUNICORN_BACKEND_PID_DIR'), 'gunicorn.pid')
timeout = 700
accesslog = os.path.join(env('GUNICORN_BACKEND_LOG_DIR'), 'gunicorn_access.log')
errorlog = os.path.join(env('GUNICORN_BACKEND_LOG_DIR'), 'gunicorn_error.log')
user = env('DEFAULT_USER')
umask = 755
