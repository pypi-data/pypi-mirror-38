# -*- coding: utf-8 -*-
from distutils.core import setup

modules = \
['django_postgres_unlimited_varchar']
install_requires = \
['django>=2.0,<3.0']

setup_kwargs = {
    'name': 'django-postgres-unlimited-varchar',
    'version': '1.0',
    'description': 'A tiny app adding support unlimited varchar fields in Django/Postgres.',
    'long_description': None,
    'author': 'Jacob Kaplan-Moss',
    'author_email': 'jacob@jacobian.org',
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
