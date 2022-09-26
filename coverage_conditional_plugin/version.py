from typing import Optional, Tuple

try:  # pragma: no cover
    from importlib.metadata import version as metadata_version
except ImportError:  # pragma: no cover
    from importlib_metadata import version as metadata_version  # type: ignore

from packaging import version


def package_version(
    package: str,
) -> Optional[Tuple[int, ...]]:
    """
    Helper function that fetches distribution version.

    Can throw multiple exceptions.
    Be careful, use ``is_installed`` before using this one.

    Returns parsed varsion to be easily worked with.
    """
    return version.parse(metadata_version(package)).release
