from .common import *

SECRET_KEY = 'development-secret-key'
DEBUG = True
ALLOWED_HOSTS = ['*']

HAYSTACK_CONNECTIONS['default']['URL'] = 'http://elasticsearch_local:9200/'