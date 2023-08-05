import os, sys
import importlib.util

from axju.core.basic import BasicWorker
from axju.worker.django.settings import STEPS

class DjangoWorker(BasicWorker):
    """This class load the django settings"""

    APP_PIP = {
        'crispy_forms': 'django-crispy-forms',
        'debug_toolbar': 'django-debug-toolbar',
    }

    DEFAULT_SETTINGS = [
        '', 'development', 'production'
    ]

    def __init__(self, folder='.', setting=''):
        super(DjangoWorker, self).__init__(steps=STEPS, templates=('axju', 'worker/django/templates/'))

        print( folder, setting)

        self.folder = os.path.abspath(folder)
        self.project = os.path.basename(self.folder)

        sys.path.append(self.folder)
        self.settings = self.__load_settings(setting)

    def __str__(self):
        return '>>{}<< {}'.format(self.project, self.folder)

    def render_data(self):
        data = super(DjangoWorker, self).render_data()

        data['folder'] = self.folder
        data['project'] = self.project

        if self.settings:
            data['setting'] = self.settings.__name__
            data['settings'] = self.settings

            if getattr(self.settings, 'DATABASES', None):
                data['db'] = self.settings.DATABASES.get('default')

            if getattr(self.settings, 'HOST', None):
                data['host'] = self.settings.HOST

            if 'host' not in data and getattr(self.settings, 'ALLOWED_HOSTS', None):
                data['host'] = self.settings.ALLOWED_HOSTS[0]

        return data

    def __load_settings(self, setting):
        """Load the django settings. For single module settings == '', overwise
        mean multiple settings. First check if the setting exist. If not,try to
        load the default settings."""

        settings_list = self.find_settings()
        setting_name = setting

        if setting not in settings_list:
            self.logger.debug('No settings named "%s"', setting)

            for default in self.DEFAULT_SETTINGS:
                if default in settings_list:
                    setting_name = default
                    break

        s = '{}.settings'.format(self.project)
        if setting_name: s += '.{}'.format(setting_name)

        self.logger.debug('Load "%s" as the setting module', s)
        return __import__(s, fromlist=[''])


    def find_settings(self):
        """Looking for multiple settings"""
        settings = []
        if os.path.isfile(os.path.join(self.folder, self.project, 'settings.py')):
            settings.append(''.format(self.project))

        elif os.path.isdir(os.path.join(self.folder, self.project, 'settings')):
            for setting in os.listdir(os.path.join(self.folder, self.project, 'settings')):
                if os.path.isfile(os.path.join(os.path.join(self.folder, self.project, 'settings'), setting)):
                    settings.append(os.path.splitext(setting)[0])

        return settings

    def install_requirement(self):
        """Check the settings for dependencies and install thay"""
        packages = []

        for app in self.settings.INSTALLED_APPS:
            if app in self.APP_PIP:
                packages.append(self.APP_PIP[app])

        if self.settings.DATABASES['default']['ENGINE'] == 'django.db.backends.postgresql':
            packages.append('psycopg2-binary')

        try:
            if self.settings.EMAIL_BACKEND == 'django.core.mail.backends.smtp.EmailBackend':
                packages.append('django_smtp_ssl')
        except:
            self.logger.exception('No email backendd')

        if packages:
            self.execute([
                'cd {}'.format(self.folder),
                'python3 -m venv venv',
                'source venv/bin/activate',
                'pip install --upgrade {}'.format(' '.join(packages)),
                'deactivate',
            ])

    def setup_db(self):
        """Setup the right DB"""
        config = self.settings.DATABASES['default']
        engine = config['ENGINE']

        if engine == 'django.db.backends.postgresql':
            self.run('postgresql')
