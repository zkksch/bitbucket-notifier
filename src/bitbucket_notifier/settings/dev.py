from .base import *


DEBUG = True
SECRET_KEY = 'hc6yy72c99*z8zv4j_&dux(23przbl62bmjwmyg1ucmsioks$v'
AUTH_PASSWORD_VALIDATORS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(os.path.dirname(BASE_DIR), 'db.sqlite3'),
    }
}

ALLOWED_HOSTS = '*'
