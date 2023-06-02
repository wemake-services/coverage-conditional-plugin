import os
import sys
import traceback
from importlib import import_module
from typing import Any, ClassVar, Dict, List, Tuple, Union

from coverage import CoveragePlugin
from coverage.config import CoverageConfig
from packaging.markers import default_environment

from coverage_conditional_plugin.version import package_version

#: Used for `omit` specification.
_OmitConfigSpec = Dict[str, Union[str, List[str]]]

_INI_OMIT_ERROR = (
    'Improperly configured: `ini` does not ' +
    'support `omit` specification, ' +
    'current setting is: {0}'
)


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
    # We use `exlude_line` and not `exclude_also`,
    # because settings are already post-processed, which means that
    # `exlude_line` and `exclude_also` are already joined:
    _ignore_opt_name: ClassVar[str] = 'report:exclude_lines'
    _omit_opt_name_plugin: ClassVar[str] = 'coverage_conditional_plugin:omit'
    _omit_opt_name_coverage: ClassVar[str] = 'run:omit'

    def configure(  # type: ignore[override]
        self, config: CoverageConfig,
    ) -> None:
        """
        Main hook for adding extra configuration.

        Part of the ``coverage`` public API.
        Called right after ``coverage_init`` function.
        """
        self._configure_omits(config)
        self._configure_rules(config)

    def _configure_omits(self, config: CoverageConfig) -> None:
        omits: Union[str, _OmitConfigSpec, None] = _get_option(
            config,
            self._omit_opt_name_plugin,
        )
        if omits is None:
            return  # No setting, ignoring
        elif not isinstance(omits, dict):
            raise RuntimeError(_INI_OMIT_ERROR.format(omits))

        for code, patterns in omits.items():
            if isinstance(patterns, str):
                patterns = [patterns]
            if _should_be_applied(code):
                self._omit_pattern(config, patterns)

    def _configure_rules(self, config: CoverageConfig) -> None:
        try:  # ini format
            rules = filter(
                bool,
                _get_option(config, self._rules_opt_name).splitlines(),
            )
        except AttributeError:  # toml format
            rules = _get_option(config, self._rules_opt_name).items()

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
        if _should_be_applied(code):
            self._ignore_marker(config, marker)

    def _ignore_marker(
        self, config: CoverageConfig, marker: str,
    ) -> None:
        """Adds a marker to the ignore list."""
        exclude_lines = _get_option(config, self._ignore_opt_name)
        exclude_lines.append(marker)
        config.set_option(self._ignore_opt_name, exclude_lines)

    def _omit_pattern(
        self, config: CoverageConfig, patterns: List[str],
    ) -> None:
        """Adds a file name pattern to the omit list."""
        omit_patterns = _get_option(config, self._omit_opt_name_coverage)
        omit_patterns.extend(patterns)
        config.set_option(self._omit_opt_name_coverage, omit_patterns)


def _is_installed(package: str) -> bool:
    """Helper function to detect if some package is installed."""
    try:
        import_module(package)
    except ImportError:
        return False
    return True


def _should_be_applied(code: str) -> bool:
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


def _get_option(  # type: ignore[misc]
    config: CoverageConfig, option: str,
) -> Any:
    # Hack to silence all new typing issues.
    return config.get_option(option)


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
