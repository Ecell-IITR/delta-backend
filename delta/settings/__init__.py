import os

from .base import *

env = os.environ.get('ENVIRONMENT')
print('Checking working environment: ', env)
if env == 'production':
    from .deployment import *
else:
    from .development import *
