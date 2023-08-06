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
    'version': '0.2.0',
    'description': 'Implementation of Spring Boot Actuator and Spring Cloud Discovery, Security and Tracing',
    'long_description': "# Eureka Client for Python\n\n```yaml\ninstance:\n  instanceId: localhost:testclient:8080\n  hostName: localhost\n  app: testclient\n  ipAddr: 127.0.0.1\n  vipAddress: testclient\n  secureVipAddress: testclient\n  status: UP\n  port:\n    $: 8080\n    '@enabled': 'true'\n  securePort:\n    $: 443\n    '@enabled': 'false'\n  statusPageUrl: http://localhost:8080/info\n  homePageUrl: None\n  healthCheckUrl: None\n  dataCenterInfo:\n    '@class': com.netflix.appinfo.InstanceInfo$DefaultDataCenterInfo\n    name: MyOwn\n\neureka:\n  host: localhost\n  port: 9091\n  ssl: false\n  servicePath: solenoid\n  \noptions:\n  requestImpl: requests\n  maxRetries: 3\n  heartBeatIntervalInSecs: 30\n  registryFetchIntervalInSecs: 30\n  registerWithEureka: true\n\n```\n",
    'author': 'Grant McDonald',
    'author_email': 'grantmmcdonald@gmail.com',
    'url': 'https://github.com/calmseas/solenoid',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
