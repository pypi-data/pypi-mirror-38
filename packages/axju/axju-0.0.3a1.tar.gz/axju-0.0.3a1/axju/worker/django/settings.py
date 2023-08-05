"""This file contains some defaults for the django worker"""

STEPS = {
    'run': {
        'info': 'Run all steps',
        'steps': ['prepare', 'requirement', 'setupdb', 'project', 'nginx'],
    },
    'prepare': {
        'info': 'Prepare the system',
        'commands': [
            'sudo apt update -y',
            'sudo apt upgrade -y',
            'sudo apt install -y python3-dev python3-pip python3-venv',
            'sudo apt autoremove -y',
            'sudo -H pip3 install --upgrade pip',
            'cd {{ folder }}',
            'python3 -m venv venv',
            'source venv/bin/activate',
            'pip install --upgrade pip wheel django python-decouple',
            'deactivate',
        ]
    },
    'postgresql': {
        'info': 'Setup a postgresql DB.',
        'template': 'postgresql.template'
    },
    'project': {
        'info': 'Setupthe project, migrate db and collectstatic',
        'template': 'project.template'
    },
    'setupdb': {
        'info': 'Setup the DB.',
        'func': 'setup_db',
    },
    'requirement': {
        'info': 'Install the project requirements.',
        'func': 'install_requirement',
    },
    'nginx': {
        'info': 'setup everything for nginx',
        'steps': ['nginx-install', 'nginx-file', 'nginx-setup']
    },
    'nginx-install': {
        'info': 'Install nginx',
        'commands': ['sudo apt -y install nginx'],
    },
    'nginx-file': {
        'info': 'Create the nginx config file',
        'template': 'nginx-config.template',
        'filename': '/etc/nginx/sites-available/{{ project }}',
        'sudo': True,
    },
    'nginx-setup': {
        'info': 'Compile the config file and start nginx',
        'template': 'nginx-setup.template',
    },
    'gunicorn': {
        'steps': ['gunicorn-install', 'gunicorn-file', 'gunicorn-setup'],
    },
    'gunicorn-install': {
        'template': 'gunicorn-install.template',
    },
    'gunicorn-file': {
        'template': 'gunicorn-file.template',
        'filename': '{{ folder }}/gunicorn_start',
    },
    'gunicorn-setup': {
        'commands': [
            'chmod u+x {{ folder }}/gunicorn_start',
            'mkdir {{ folder }}/run',
            'mkdir {{ folder }}/logs',
            'touch {{ folder }}/logs/gunicorn.log'
        ],
    },
}
