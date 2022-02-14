#
# Settings used by pytest
#

# Import all general settings
from .settings import *

# Override below

DATABASES = {
    'default': { 'ENGINE': 'django.db.backends.sqlite3' }
}
