# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['lhub_integ']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<7.1', 'dataclasses-json', 'docstring-parser>=0.1,<0.2']

entry_points = \
{'console_scripts': ['bundle-requirements = '
                     'lhub_integ.bundle_requirements:main']}

setup_kwargs = {
    'name': 'lhub-integ',
    'version': '0.1.2',
    'description': 'The Logichub Integration SDK',
    'long_description': '# lhub_integ\nPython package to shim basic scripts to work with integration machinery. An example script is available in `/lhub_integ/tests/test_integration/main.py`\nThis package requires Python 3.6:\n```\n# Optional: install Python 3.6 with pyenvv\nbrew install pyenv\npyenv install 3.6.6\npyenv init # Follow the instructions\npyenv local 3.7.1\n# Make sure this says "3.7.1"\npython --version\n```\n\n## Usage (as an integration writer)\nTo write a Python script that is convertible into an integration:\n\n1. Create a directory that will contain your integration\n2. Install lhub_integ as a local package:\n```pip install lh_integration```\n3. Copy `main.py` from the tests folder into your integration and modify as desired.\n\nPython scripts must provide an entrypoint function with some number of arguments. These arguments will correspond to columns\nin the input data. The function should return a Python dictionary that can be serialized to JSON\n\n```python\ndef process(url, num_bytes: int):\n  return {\'output\': url + \'hello\'}\n```\n\n# Dev Installation\n```\n# Get Python 3\nbrew install python\nbrew install pipenv\npipenv install\npipenv shell\n```\n\n# Test the package installer\n```\npipenv install -e .\n```\n\n# Run tests\n```pytest```\n\n# Deploying changes to lhub_integ & custom integrations\n1. Make changes. Verify that the tests pass and that you can build the image locally (do not push the image from your laptop)\n2. Get your changes merged to master. `CircleCI` will build an image. It will be unused at this point because nothing\npoints to `latest`.\n3. Go to https://hub.docker.com/r/logichub/integrations-custom/tags/ and find that latest tag that contains the results of building your image. Update `ConfigProperties.IntegrationsCustomImageTag` and make any code updates\nrequired.\n\n',
    'author': 'Russell Cohen',
    'author_email': 'russell@logichub.com',
    'url': 'https://logichub.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
