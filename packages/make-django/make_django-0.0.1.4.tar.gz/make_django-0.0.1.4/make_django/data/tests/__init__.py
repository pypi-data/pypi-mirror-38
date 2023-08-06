import re
import os
from pathlib import Path
from django.conf import settings


def import_module(module_path):
    module = __import__(module_path, globals(), locals(), ['*'])
    for k in dir(module):
        locals()[k] = getattr(module, k)


for app in settings.INSTALLED_APPS:
    if app.startswith('apps.'):
        print('search tests in', app)
        for path in Path.iterdir(Path(f'{app}/tests'.replace('.', '/'))):
            if path.is_file() and re.match(r'^test_.*\.py$', path.name):
                test = re.sub(r'\.py$', '', str(path).replace(os.path.sep, '.'))
                print('import', test)
                exec(f'from {test} import *')
