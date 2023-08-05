# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['django_fast_migrations',
 'django_fast_migrations.management',
 'django_fast_migrations.management.commands']

package_data = \
{'': ['*']}

install_requires = \
['django>=1.8']

setup_kwargs = {
    'name': 'django-fast-migrations',
    'version': '0.1.0',
    'description': '',
    'long_description': '[![Downloads](https://pepy.tech/badge/django-fast-migrations)](https://pepy.tech/project/django-fast-migrations)\n\n# Django-Fast-Migrations\n\nCommand to speed up the application of migrations in a Django project.\n\n\n## Installation\n\nInstall using pip:\n\n```\npip install django-fast-migrations\n```\n\nThen add ``\'django_fast_migrations\'`` to your ``INSTALLED_APPS``.\n\n```\nINSTALLED_APPS = [\n    ...\n    \'django_fast_migrations\',\n]\n```\n\n## Usage\n\nHow to execute command:\n\n    ./manage.py migrate_by_app\n    \nThe previous command only checks if there are applications with pending migrations.\n\nTo execute the pending migrations we have to call the command:\n\n    ./manage.py migrate_by_app\n\nWhen executed without parameters it **only checks** if there are applications with pending migrations\n\nPossible arguments:\n\n* ```--execute```: If pending migrations are found then execute them.\n* ```--database```: Nominates a database to synchronize. Defaults to the "default" database.\n\n',
    'author': 'Andreu Vallbona',
    'author_email': 'avallbona@apsl.net',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
}


setup(**setup_kwargs)
