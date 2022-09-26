import os
import sys
import traceback
from importlib import import_module
from typing import ClassVar, Dict, Iterable, Tuple, Union

from coverage import CoveragePlugin
from coverage.config import CoverageConfig
from packaging.markers import default_environment

from coverage_conditional_plugin.version import package_version


def get_env_info() -> Dict[str, object]:
    """Public helper to get the same env we pass to the plugin."""
    env_info: Dict[str, object] = {}
    env_info.update(default_environment())
    # Feel free to send PRs that extend this dict:
    env_info.update({
        'sys_version_info': sys.version_info,
        'os_environ': os.environ,
        'is_installed': _is_installed,
        'package_version': package_version,
        # We need this, otherwise `_should_be_applied` can generate a warning:
        'sys': sys,
    })
    return env_info


class _ConditionalCovPlugin(CoveragePlugin):
    _rules_opt_name: ClassVar[str] = 'coverage_conditional_plugin:rules'
    _ignore_opt_name: ClassVar[str] = 'report:exclude_lines'

    def configure(self, config: CoverageConfig) -> None:
        """
        Main hook for adding extra configuration.

        Part of the ``coverage`` public API.
        Called right after ``coverage_init`` function.
        """
        rules: Iterable[str]

        try:  # ini format
            rules = filter(
                bool,
                config.get_option(self._rules_opt_name).splitlines(),
            )
        except AttributeError:  # toml format
            rules = config.get_option(self._rules_opt_name).items()

        for rule in rules:
            self._process_rule(config, rule)

    def _process_rule(
        self, config: CoverageConfig, rule: Union[str, Tuple[str, str]],
    ) -> None:
        if isinstance(rule, str):
            code, marker = [part.strip() for part in rule.rsplit(':', 1)]
            code = code[1:-1]  # removes quotes
        elif isinstance(rule, tuple):
            marker = rule[0]
            code = rule[1]
        else:
            raise ValueError("Invalid type for 'rule'.")
        if self._should_be_applied(code):
            self._ignore_marker(config, marker)

    def _should_be_applied(self, code: str) -> bool:
        """
        Determines whether some specific marker should be applied or not.

        Uses ``exec`` on the code you pass with the marker.
        Be sure, that this code is safe.

        We also try to provide useful global functions
        to cover the most popular cases, like:

        - python version
        - OS name, platform, and version
        - helpers to work with installed packages

        Some examples:

        .. code:: ini

          [coverage:coverage_conditional_plugin]
          rules =
            "sys_version_info >= (3, 8)": py-gte-38
            "is_installed('mypy')": has-mypy

        So, code marked with `# pragma: py-gte-38` will be ignored
        for all version of Python prior to 3.8 release.
        And at the same time,
        this code will be included to the coverage on 3.8+ releases.

        """
        env_info = get_env_info()
        try:
            return eval(code, env_info)  # noqa: WPS421, S307
        except Exception:
            msg = 'Exception during conditional coverage evaluation:'
            print(msg, traceback.format_exc())  # noqa: WPS421
            return False

    def _ignore_marker(self, config: CoverageConfig, marker: str) -> None:
        """Adds a marker to the ignore list."""
        exclude_lines = config.get_option(self._ignore_opt_name)
        exclude_lines.append(marker)
        config.set_option(self._ignore_opt_name, exclude_lines)


def _is_installed(package: str) -> bool:
    """Helper function to detect if some package is installed."""
    try:
        import_module(package)
    except ImportError:
        return False
    return True


def coverage_init(reg, options) -> None:
    """
    Entrypoint, part of the ``coverage`` API.

    This is called when we specify:

    .. code:: ini

      [coverage:run]
      plugins =
        coverage_conditional_plugin

    See also:
        https://coverage.readthedocs.io/en/latest/plugins.html

    """
    reg.add_configurer(_ConditionalCovPlugin())
