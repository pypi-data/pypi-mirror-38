from .base import *
from .main import *
from pathlib import Path
import importlib.util


def import_module(module_name):
    module_spec = importlib.util.find_spec(module_name)
    if module_spec:
        module = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(module)

        for attr_name in dir(module):
            if not attr_name.startswith('__'):
                locals()[attr_name] = getattr(module, attr_name)
                globals()[attr_name] = getattr(module, attr_name)


for item in Path('./application/settings').iterdir():
    if not item.is_dir() and not item.name.startswith('__') and item.stem not in ('base', 'main'):
        import_module(f'application.settings.{item.stem}')
