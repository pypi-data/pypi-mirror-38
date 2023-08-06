"""
Python module boilerplate
"""
import os

try:
    from .version import __version__, version_info
except ImportError:
    version_info = (0, 0, 0, 0, 'a')
    __version__ = '{}.{}.{}+{}'.format(*version_info)


MODULE_PATH = os.path.abspath(os.path.dirname(__file__))


__author__ = 'Alexander Vasin'
__email__ = 'hi@alvass.in'
__license__ = 'Proprietary License',
__maintainer__ = __author__  # It's same persons right now
__status__ = 'Production'

__all__ = (
    '__author__', '__email__', '__license__', '__maintainer__',
    '__version__', '__status__', 'MODULE_PATH', 'version_info',
)
