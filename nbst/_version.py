"""
This module contains project version information.

.. currentmodule:: nbst._version
.. moduleauthor:: Stephen Eaton <seaton@strobotics.com.au>
"""
from importlib_metadata import version

__version__ = version(__package__)

__all__ = ("__version__",)
