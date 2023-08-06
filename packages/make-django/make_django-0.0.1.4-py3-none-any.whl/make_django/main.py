import os
import sys
import subprocess
from redbaron import RedBaron
from make_django.lib.path_util import Path
from make_django.lib.paths_keeper import PathsKeeper
from make_django.lib.files_util import process_files
from make_django.batteries import load_batteries


__name__ = 'make_django'
__author__ = 'filantus'
__version__ = '0.0.1.4'
__doc__ = 'Tool for rapid making django projects'


class DjangoMaker:
    project_name = None

    paths = PathsKeeper()
    paths.self = Path(__file__).parent
    paths.data = paths.self/'data'
    paths.project = Path().cwd()
    paths.virtual_env = paths.project/'.venv'
    paths.python = paths.virtual_env/'Scripts/python.exe'
    paths.pip = paths.virtual_env/'Scripts/pip'
    paths.django_admin = paths.virtual_env/'Lib/site-packages/django/bin/django-admin.py'
    paths.application = paths.project/'application'

    def __init__(self, args):
        if len(args) == 0:
            print('project_name positional argument required!')
            sys.exit()

        if self.paths.project == self.paths.project.parent:
            print('project path must be not root!')
            sys.exit()

        self.args = args
        self.project_name = args[0]
        self.paths.settings = self.paths.project.j('application/settings')
        self.paths.app = self.paths.project/f'apps/{self.project_name}'
        self.paths.app_templates = self.paths.app/f'templates/{self.project_name}/'
        self.paths.app_static = self.paths.app/f'static/{self.project_name}/'
        print('\nPaths:\n', self.paths, '\n', sep='')
        self.clean()

        self.batteries = [b(self) for b in load_batteries()]
        for battery in self.batteries:
            if battery.arg in self.args:
                battery.arg_found = True

    def clean(self):
        if '+clean' in self.args or '+clean-full' in self.args:
            for item in self.paths.project.iterdir():
                if item.name != '.venv' or '+clean-full' in self.args:
                    item.delete()

    def freeze_requirements(self):
        completed_process = subprocess.run(f'"{self.paths.pip}" freeze', shell=True, capture_output=True, check=True)
        self.paths.project.j('requirements.txt').write_bytes(completed_process.stdout)

    def make_virtualenv(self):
        os.system('virtualenv .venv')
        os.system(f'{self.paths.project} -V')
        os.system(f'{self.paths.project} -m pip install --upgrade pip --force-reinstall')
        os.system(f'{self.paths.pip} install --upgrade setuptools --force-reinstall')

    def install_package(self, package_name):
        os.system(f'{self.paths.pip} install {package_name}')

    def install_packages(self):
        packages = [
            'django',
        ]

        for battery in self.batteries:
            if battery.arg in self.args:
                for package in battery.packages:
                    packages.append(package)

        for package in packages:
            self.install_package(package)

    def make_project(self):
        print('\nmake project')
        os.system(f'"{self.paths.python} {self.paths.django_admin}" startproject application')

        self.paths.application.unpack_dir()
        self.paths.application.j('settings.py').rename('base.py')
        self.paths.data.copy_item('application', self.paths.project)
        self.paths.application.j('base.py').replace(self.paths.settings/'base.py')
        self.paths.data.copy_item('tests', self.paths.project)
        self.paths.project.j('apps').mkdir()
        self.paths.project.j('public/assets').mkdir()

        for battery in self.batteries:
            if battery.arg in self.args:
                battery.copy_settings()

    def make_app(self):
        print('\nmake app')
        os.system(f'{self.paths.python} manage.py startapp {self.project_name}')
        self.paths.project.move_item(self.project_name, './apps')
        self.paths.app.j(f'tests.py').unlink()
        self.paths.app.j(f'views.py').unlink()
        self.paths.data.copy_item('app', self.paths.project/f'apps/{self.project_name}', join_item=False)

        for dir_name in ('static', 'templates'):
            self.paths.app.j(dir_name).rename(f'_{dir_name}')
            self.paths.app.j(f'_{dir_name}').replace(self.paths.app/f'{dir_name}/{self.project_name}')

    def patch_settings(self):
        settings_path = self.paths.settings/'main.py'
        red = RedBaron(settings_path.read_text())

        # Apps
        apps_list = []

        for battery in self.batteries:
            if battery.arg in self.args:
                for app in battery.apps:
                    apps_list.append(app)

        apps_list.append(f'apps.{self.project_name}')

        apps = red.find("assignment", target=lambda x: x.dumps() == "INSTALLED_APPS").value
        value = ['\n']
        for app in reversed(apps_list):
            value.insert(0, f"   '{app}',")
            value.insert(0, '\n')

        apps.value = value

        text = red.dumps()

        for battery in self.batteries:
            red, text = battery.patch_settings(red, text)

        settings_path.write_text(self.clean_blank_lines(text))

    def patch_urls(self):
        # application urls
        urls_path = self.paths.application/'urls.py'
        red = RedBaron(urls_path.read_text())

        import_node = red.find('FromImportNode', lambda n: 'from django.urls import' in str(n))
        import_node.targets.append('include')

        urlpatterns = red.find("assignment", target=lambda x: x.dumps() == "urlpatterns").value
        urlpatterns.append(f"    path('', include('apps.{self.project_name}.urls')),")

        urls_path.write_text(red.dumps())

        # app urls
        urls_path = self.paths.app/'urls.py'
        red = RedBaron(urls_path.read_text())
        # urlpatterns = red.find("assignment", target=lambda x: x.dumps() == "urlpatterns").value

        text = red.dumps()

        for battery in self.batteries:
            red, text = battery.patch_urls(red, text)

        urls_path.write_text(self.clean_blank_lines(text))

    def batteries_deploy(self):
        for battery in self.batteries:
            battery.final_patch()
            battery.deploy()

    def _process_macros(self, path):
        f = Path(path)

        if str(self.paths.virtual_env) in str(f):
            return

        content = f.read_bytes()
        content = content.replace(b'%DM_PROJECT_NAME%', self.project_name.encode())
        f.write_bytes(content)

    def process_macros(self):
        print('\nprocess macros')
        process_files(str(self.paths.project), self._process_macros)

    @staticmethod
    def clean_blank_lines(text):
        while '\n'*3 in text:
            text = text.replace('\n'*3, '\n')
        return text


def main(args=None):
    if args is None:
        args = sys.argv[1:]
    print('make_django args:', args)

    dm = DjangoMaker(args)
    if '-venv' not in args:
        dm.make_virtualenv()
        dm.install_packages()
        dm.freeze_requirements()
    dm.make_project()
    dm.make_app()
    dm.patch_settings()
    dm.patch_urls()
    dm.batteries_deploy()
    dm.process_macros()

    if '+run' in args:
        try:
            os.system(f'{dm.paths.python} manage.py runserver')
        except KeyboardInterrupt:
            print('exit')


# TODO fix crlf
