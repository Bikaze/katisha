import os
from .common import *  # noqa: F403

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
ALLOWED_HOSTS = []
SECRET_KEY = os.environ.get('SECRET_KEY')