"""The mind-blowing main package!"""

from ._get_hello import get_hello

try:
    from ._version import version as __version__
    from ._version import version_tuple
except ImportError:
    __version__ = "unknown version"
    version_tuple = (0, 0, "unknown version")

__all__ = [
    "get_hello",
]
