import os, sys
import getpass
import logging
import subprocess
import tempfile
from jinja2 import Environment, BaseLoader, PackageLoader


class StepWorker(object):
    """The basic worker"""

    steps = {}

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.debug('create the object')

    def execute(self, commands):
        """Connect to the shell and execute multiple commands. It is necessary
        to activate a virtual environment and then install some packages."""

        cmd = ['/bin/bash', '-i']
        encoding = 'utf-8'
        if sys.platform[:3] == 'win':
            cmd = ['cmd']
            encoding = 'cp437'
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

        for command in commands:
            self.logger.debug('run command "%s"', command)
            p.stdin.write(str(command + "\n").encode())
            p.stdin.flush()

        p.stdin.close()
        self.logger.info('working...')
        self.logger.debug('result:\n%s', p.stdout.read().decode(encoding))
        p.wait()

    def render_data(self):
        return {
            'user': getpass.getuser(),
        }

    def render_str(self, s):
        template = Environment(loader=BaseLoader()).from_string(s)
        return template.render(self.render_data())

    def render_commands(self, commands):
        """Render a list of commands. That can contain some dummy."""
        return [ self.render_str(c) for c in commands ]

    def show(self):
        """Display some infos about the steps."""
        n = max([ len(s) for s in self.steps ])
        for step, data in self.steps.items():
            print(step.ljust(n+1, '.'), data.get('info', 'missing'), sep='')

    def run_step(self, name):
        """Run the one step"""
        if name not in self.steps:
            self.logger.warning('No step definition for "%s"', name)
            return None

        step = self.steps[name]
        self.logger.info('run step "%s"', name)

        if 'commands' in step:
            self.execute(self.render_commands(step['commands']))

        elif 'func' in step:
            getattr(self, step['func'])(**step.get('kwargs', {}))

        elif 'steps' in step:
            for s in step['steps']:
                self.run_step(s)
            self.logger.info('finished step "%s"', name)

        return step


class TemplateWorker(StepWorker):
    """..."""

    templates = None

    def __init__(self):
        super(TemplateWorker, self).__init__()
        self.templateEnv = self.setup_template_env()

    def setup_template_env(self, **kwargs):
        templates = kwargs.get('templates')
        if templates: self.templates = templates

        if self.templates:
            templateLoader = PackageLoader(*self.templates)
            return Environment(loader=templateLoader)
        return None

    def render_template(self, filename):
        template = self.templateEnv.get_template(filename)
        return template.render(self.render_data())

    def run_step(self, name):
        step = super(TemplateWorker, self).run_step(name)

        if not step: return None

        if 'template' in step:
            t = self.render_template(step['template'])

            if 'filename' in step:
                filename = self.render_str(step['filename'])

                with tempfile.NamedTemporaryFile() as f:
                    f.write(t.encode())
                    f.flush()
                    if step.get('sudo', False):
                        subprocess.call(['sudo', 'cp', f.name, filename])
                    else:
                        subprocess.call(['cp', f.name, filename])

            else:
                self.execute(t.split('\n'))
            self.logger.info('finished step "%s"', name)

        return step
