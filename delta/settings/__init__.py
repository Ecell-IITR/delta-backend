import os

from .base import *

env = os.environ.get('ENVIRONMENT')
if env == 'production':
    from .deployment import *
else:
    from .development import *
