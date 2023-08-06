[![Build Status](https://api.travis-ci.com/DavidCain/mitoc-const.svg?branch=master)](https://travis-ci.com/DavidCain/mitoc-const/)
[![PyPI version](https://img.shields.io/pypi/v/mitoc-const.svg)](https://pypi.python.org/pypi/mitoc-const)

# MITOC Constants
This is a set of constants for use across MIT Outing Club infrastructure.

MITOC has a number of projects, many of which reference values used
in other databases or deployed projects. These projects may be deployed
separately, so there's value in having shared values at constants in an
external package.

### Releasing a new version
First, augment the version in `setup.py`. Then:

```bash
rm -rf dist/ build/ mitoc_const.egg-info/
pipenv run python setup.py sdist bdist_wheel
pipenv run twine upload dist/*
git push origin master
```
