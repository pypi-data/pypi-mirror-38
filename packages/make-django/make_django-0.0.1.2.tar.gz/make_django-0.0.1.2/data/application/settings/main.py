from .base import *
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

ENV = os.environ.get('ENV', 'development')

DEBUG = ENV != 'production'

HOST = 'https://my_site_production.domain' if ENV == 'production' else 'http://127.0.0.1'

ALLOWED_HOSTS = ['localhost', HOST.split('//')[-1]]

INTERNAL_IPS = (
    '127.0.0.1',
)


INSTALLED_APPS += []


TEMPLATES[0]['DIRS'] = [
    os.path.join(BASE_DIR, 'application', 'templates'),
]
TEMPLATES[0]['OPTIONS']['builtins'] = [
    'application.templatetags.filters',
]


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'public', 'assets')
