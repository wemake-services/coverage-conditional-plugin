# coverage-conditional-plugin

[![wemake.services](https://img.shields.io/badge/%20-wemake.services-green.svg?label=%20&logo=data%3Aimage%2Fpng%3Bbase64%2CiVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAABGdBTUEAALGPC%2FxhBQAAAAFzUkdCAK7OHOkAAAAbUExURQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP%2F%2F%2F5TvxDIAAAAIdFJOUwAjRA8xXANAL%2Bv0SAAAADNJREFUGNNjYCAIOJjRBdBFWMkVQeGzcHAwksJnAPPZGOGAASzPzAEHEGVsLExQwE7YswCb7AFZSF3bbAAAAABJRU5ErkJggg%3D%3D)](https://wemake.services)
[![Build Status](https://travis-ci.com/wemake-services/coverage-conditional-plugin.svg?branch=master)](https://travis-ci.com/wemake-services/coverage-conditional-plugin)
[![Python Version](https://img.shields.io/pypi/pyversions/coverage-conditional-plugin.svg)](https://pypi.org/project/coverage-conditional-plugin/)
[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)

Conditional coverage based on any rules you define!

Some project have different parts that relies on different environments:

- Python version, some code is only executed on specific versions and ignored on others
- OS version, some code might be Windows, Mac, or Linux only
- External packages, some code is only executed when some 3rd party package is installed

Current best practice is to use `# pragma: no cover` for this places in our project.
This project allows to use configurable pragmas 
that include code to the coverage if some condition evaluates to true, 
and fallback to ignoring this code when condition is false.


## Installation

```bash
pip install coverage-conditional-plugin
```

Then you will need to add to your `setup.cfg` or `.coveragerc` file 
some extra configuration:

```ini
[coverage:run]
# Here we specify plugins for coverage to be used:
plugins =
  coverage_conditional_plugin

[coverage:coverage_conditional_plugin]
# Here we specify our pragma rules:
rules =
  "sys_version_info >= (3, 8)": py-gte-38
  "is_installed('mypy')": has-mypy

```

Adapt rules to suit your needs!


## Example

Imagine that we have this code:

```python
try:  # pragma: has-django
    import django
except ImportError:  # pragma: has-no-django
    django = None

def run_if_django_is_installed():
    if django is not None:  # pragma: has-django
        ...
```

And here's the configuration you might use:

```ini
[coverage:coverage_conditional_plugin]
rules =
  "is_installed('django')": has-django
  "not is_installed('django')": has-no-django

```

When running tests with and without `django` installed 
you will have `100%` coverage in both cases.

But, different lines will be included. 
With `django` installed it will include 
both `try:` and `if django is not None:` conditions.

When running without `django` installed,
it will include `except ImportError:` line.


## Writting pragma rules

Format for pragma rules is: 

```
"pragma-condition": pragma-name
```

Code inside `"pragma-condition"` is evaluted with `eval`.
Make sure that the input you pass there is trusted!
`"pragma-condition"` must return `bool` value after evaluation.

We also provide a bunch of helpers to make writing rules easier:

- `sys_version_info` is the same as [`sys.version_info`](https://docs.python.org/3/library/sys.html#sys.version_info)
- `os_name` is the same as [`os.name`](https://docs.python.org/3/library/os.html#os.name)
- `os_environ` is the same as [`os.environ`](https://docs.python.org/3/library/os.html#os.environ)
- `platform_system` is the same as [`platform.system()`](https://docs.python.org/3/library/platform.html#platform.system)
- `platform_release` is the same as [`platform.release()`](https://docs.python.org/3/library/platform.html#platform.release)
- `is_installed` is our custom function that tries to import the passed string, returns `bool` value
- `package_version` is our custom function that tries to get package version from `pkg_resources` and returns its [parsed version](https://packaging.pypa.io/en/latest/version/#packaging.version.parse)


## License

[MIT](https://github.com/wemake.services/coverage-conditional-plugin/blob/master/LICENSE)


## Credits

This project was generated with [`wemake-python-package`](https://github.com/wemake-services/wemake-python-package). Current template version is: [a61725009d8399ae77376b5ad9de354214bc1159](https://github.com/wemake-services/wemake-python-package/tree/a61725009d8399ae77376b5ad9de354214bc1159). See what is [updated](https://github.com/wemake-services/wemake-python-package/compare/a61725009d8399ae77376b5ad9de354214bc1159...master) since then.
