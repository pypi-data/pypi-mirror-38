# Copyright (c) 2014-2018 Adam Karpierz
# Licensed under the MIT License
# http://opensource.org/licenses/MIT

__all__ = ('__title__', '__summary__', '__uri__', '__version_info__',
           '__version__', '__author__', '__maintainer__', '__email__',
           '__copyright__', '__license__')

__title__        = "jtypes.pyjnius"
__summary__      = "Dynamic access to Java classes from Python (ctypes/cffi-based PyJNIus)"
__uri__          = "http://pypi.python.org/pypi/jtypes.pyjnius/"
__version_info__ = type("version_info", (), dict(serial=4,
                        major=1, minor=1, micro=4, releaselevel="beta"))
__version__      = "{0.major}.{0.minor}.{0.micro}{1}{2}".format(__version_info__,
                   dict(final="", alpha="a", beta="b", rc="rc")[__version_info__.releaselevel],
                   "" if __version_info__.releaselevel == "final" else __version_info__.serial)
__author__       = "Adam Karpierz"
__maintainer__   = "Adam Karpierz"
__email__        = "adam@karpierz.net"
__copyright__    = "Copyright (c) 2014-2018 {0}".format(__author__)
__license__      = "MIT License ; {0}".format(
                   "http://opensource.org/licenses/MIT")
