# lhub_integ
Python package to shim basic scripts to work with integration machinery. An example script is available in `/lhub_integ/tests/test_integration/main.py`
This package requires Python 3.7:
```
brew install pyenv
pyenv install 3.7.1
pyenv init # Follow the instructions
pyenv local 3.7.1
# Make sure this says "3.7.1"
python --version
```

## Usage (as an integration writer)
To write a Python script that is convertible into an integration:

1. Create a directory that will contain your integration
2. Install lhub_integ as a local package:
```pip install lh_integration```
3. Copy `main.py` from the tests folder into your integration and modify as desired.

Python scripts must provide an entrypoint function with some number of arguments. These arguments will correspond to columns
in the input data. The function should return a Python dictionary that can be serialized to JSON

```python
def process(url, num_bytes: int):
  return {'output': url + 'hello'}
```

# Dev Installation
```
# Get Python 3
brew install python
brew install pipenv
pipenv install
pipenv shell
```

# Test the package installer
```
pipenv install -e .
```

# Run tests
```pytest```

# Deploying changes to lhub_integ & custom integrations
1. Make changes. Verify that the tests pass and that you can build the image locally (do not push the image from your laptop)
2. Get your changes merged to master. `CircleCI` will build an image. It will be unused at this point because nothing
points to `latest`.
3. Go to https://hub.docker.com/r/logichub/integrations-custom/tags/ and find that latest tag that contains the results of building your image. Update `ConfigProperties.IntegrationsCustomImageTag` and make any code updates
required.

