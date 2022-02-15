#
# Settings used by pytest
#

# Import all general settings

from .settings import *
from . import env

# Override below

if env('DATABASE_URL_TEST', None):
    default = env.dj_db_url('DATABASE_URL_TEST')
else:
    default = {'ENGINE': 'django.db.backends.sqlite3'}

DATABASES = {'default': default}
