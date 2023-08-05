from .. import BaseBattery


class Rest(BaseBattery):
    arg = '+rest'
    packages = ['djangorestframework']
    apps = ['rest_framework']

    def patch_urls(self, red, text):
        if not self.arg_found:
            text = self.remove_entries(text, [
                'rest_framework',
                'router = routers.DefaultRouter(',
                'router.',
            ])
        return red, text
