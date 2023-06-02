# Version history

We follow [Semantic Versions](https://semver.org/).


## Version 0.9.0

### Features

- Adds `python@3.11` support
- Now, only `coverage@7` is officially supported
- We can now omit whole modules,
  using `[tool.coverage.coverage_conditional_plugin.omit]` feature 
  in TOML configuration files


## Version 0.8.0

### Features

- Bump `coverage` to `7.0`


## Version 0.7.0

### Features

- Use `importlib` instead of `pkg_resources` to get package version


## Version 0.6.0

### Features

- Drop `python3.6` support
- Adds `tests/` and `test_project/` to `sdist` distributions

### Misc

- Upgrades `poetry` to `1.2`


## Version 0.5.0

### Features

- `python3.10` support
- `coverage@6` support


## Version 0.4.0

### Features

- `python3.9` support

### Bugfixes

- Fixes that `packaging` restriction was too tight


## Version 0.3.1

### Bugfixes

- Adds `packaging` to the deps


## Version 0.3.0

### Features

- Now also works with configs specified in `pyproject.toml`


## Version 0.2.0

### Features

- Adds `get_env_info` function, 
  so one can import this plugin and use it programmatically 
  to debug and explore

### Misc

- Now using Github Actions
- Updates lots of dev-deps


## Version 0.1.0

- Initial release
