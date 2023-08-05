Podiant Factory Server
======================

![Build](https://git.steadman.io/podiant/factory-server/badges/master/build.svg)
![Coverage](https://git.steadman.io/podiant/factory-server/badges/master/coverage.svg)

Reliable, asynchronous media workflow manager

## Quickstart

Install Factory Server:

```sh
pip install podiant-factory-server
```

Add it to your `INSTALLED_APPS`:
```python
INSTALLED_APPS = (
    ...
    'factory_server',
    ...
)
```

Add the URL patterns:

```python
from factory_server import urls as factory_urls

urlpatterns = [
    ...
    url(r'^', include(factory_urls)),
    ...
]
```

## Running tests

Does the code actually work?

```
coverage run --source factory_server runtests.py
```

## Credits

Tools used in rendering this package:

- [Cookiecutter](https://github.com/audreyr/cookiecutter)
- [`cookiecutter-djangopackage`](https://github.com/pydanny/cookiecutter-djangopackage)
