# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['solenoid', 'solenoid.solenoids']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=3.13,<4.0',
 'flask-cors>=3.0,<4.0',
 'flask>=1.0,<2.0',
 'requests>=2.20,<3.0']

setup_kwargs = {
    'name': 'solenoid',
    'version': '0.1.0',
    'description': 'Implementation of Spring Boot Actuator and Spring Cloud Discovery, Security and Tracing',
    'long_description': None,
    'author': 'Grant McDonald',
    'author_email': 'grantmmcdonald@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
