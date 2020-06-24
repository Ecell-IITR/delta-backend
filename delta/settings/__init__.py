import os

from .base import *

env = os.environ.get('ENVIRONMENT')
print('Checking working environment: ', env)
if env == 'production':
    print('Importing production settings...')
    from .deployment import *
else:
    print('Importing development settings...')
    from .development import *
