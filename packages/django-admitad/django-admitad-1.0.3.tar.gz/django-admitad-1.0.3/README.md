# (WIP) django-admitad
[![Build Status](https://travis-ci.org/Picasel/django-admitad.svg?branch=master)](https://travis-ci.org/Picasel/django-admitad)
[![codecov](https://codecov.io/gh/Picasel/django-admitad/branch/master/graph/badge.svg)](https://codecov.io/gh/Picasel/django-admitad)
[![Python versions](https://img.shields.io/pypi/pyversions/django-admitad.svg)](https://pypi.python.org/pypi/django-admitad)
[![Pypi](https://img.shields.io/pypi/v/django-admitad.svg)](https://pypi.python.org/pypi/django-admitad)

Приложение для интеграции с Admitad CPA посредством postback-запросов

## Requirements

* [Python 3.7](https://www.python.org/downloads/release/python-370/)
* [Django 2.1.3](https://www.djangoproject.com/)

## Installation
#### via pypi
```sh
$ pip install django-admitad
```
#### via setup.py
```sh
$ python setup.py install
```

## Configuration
We need to hook django-admitad into our project.

Put admitad into your INSTALLED_APPS at settings module:
```sh
INSTALLED_APPS = (
    ...
    'admitad',
    ...
)
```
Also add some Admitad CPO secrets

```
ADMITAD_COMPAIN_CODE = 'your_compain_here'
ADMITAD_POSTBACK_KEY = 'your_key_here'
ADMITAD_POSTBACK_URL = 'https://ad.admitad.com/r'
```


## Usage
Will be soon...

## TODO
 * Celery integration
 * Test coverage (>90%)
 * Cookie handler middleware
 
## License
MIT
