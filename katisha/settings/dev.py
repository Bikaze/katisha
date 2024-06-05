from .common import *  # noqa: F403


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-q(fx3#x-02xc77x(x2nhw$$tcev%19w&nm2=p&@x%#o4qipdq8'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'katisha',
        'USER': 'bkz',
        'PASSWORD': 'k@tIsh@prOj',
        'HOST': 'localhost',
    }
}
