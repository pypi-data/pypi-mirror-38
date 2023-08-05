# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['aws_healthchecker_response']

package_data = \
{'': ['*']}

install_requires = \
['django>=1.10']

setup_kwargs = {
    'name': 'aws-healthchecker-response',
    'version': '0.1.0',
    'description': 'Django Middleware to return a 200 response to the AWS ELB HealthChecker without doing Host header checks',
    'long_description': None,
    'author': 'Matt Magin',
    'author_email': 'matt.magin@cmv.com.au',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
