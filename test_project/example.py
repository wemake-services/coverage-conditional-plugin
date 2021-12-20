from typing import Tuple


def if_gte_python310() -> Tuple[int, int]:  # pragma: py-gte-310
    """Test function for pragma ``py-gte-310``."""
    return (3, 10)


def if_gte_python39() -> Tuple[int, int]:  # pragma: py-gte-39
    """Test function for pragma ``py-gte-39``."""
    return (3, 9)


def if_gte_python38() -> Tuple[int, int]:  # pragma: py-gte-38
    """Test function for pragma ``py-gte-38``."""
    return (3, 8)


def if_gte_python37() -> Tuple[int, int]:  # pragma: py-gte-37
    """Test function for pragma ``py-gte-37``."""
    return (3, 7)


def if_gte_python36() -> Tuple[int, int]:  # pragma: py-gte-36
    """Test function for pragma ``py-gte-36``."""
    return (3, 6)


def never() -> str:  # pragma: no cover
    """Ensure that some code is never covered."""
    return 'never'


def always() -> str:
    """Test function that is always executed."""
    return 'always'


def uncovered():
    """Test function that is uncovered."""
    return 'uncovered'
