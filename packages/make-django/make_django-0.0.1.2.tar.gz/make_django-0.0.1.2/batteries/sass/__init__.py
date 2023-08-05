from .. import BaseBattery


class Sass(BaseBattery):
    arg = '+sass'
    packages = [
        'rcssmin --install-option="--without-c-extensions"',
        'rjsmin --install-option="--without-c-extensions"',
        'libsass',
        'django-compressor',
        'django-sass-processor',
    ]
    apps = ['sass_processor']

    def final_patch(self):
        if self.arg_found:
            self.dm.app_static_path.j('css/base.css').unlink()
            self.dm.app_static_path.j('css/index.css').unlink()
