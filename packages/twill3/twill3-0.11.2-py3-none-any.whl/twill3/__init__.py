# This file is part of the twill3 source distribution.
#
# twill3 is a extensible scriptlet language for testing Web apps,
# available at http://twill.idyll.org/.
#
# Contact author: C. Titus Brown, titus@idyll.org.
#
# This program and all associated source code files are Copyright (C)
# 2005-2007 by C. Titus Brown.
# 2018 by Jon Froiland.
#
# It is released under the MIT license;
# please see the included LICENSE.txt file for more information, or
# go to http://www.opensource.org/licenses/mit-license.php.

"""
twill3 Web testing language & associated utilities.
"""

__version__ = "3.11.18"

#import warnings
#warnings.defaultaction = "error"

#import pychecker.checker

__all__ = [ "TwillCommandLoop",
            "execute_file",
            "execute_string",
            "get_browser",
            "add_wsgi_intercept",
            "remove_wsgi_intercept",
            "set_output",
            "set_errout"]

#
# add extensions (twill3/extensions) and the the wwwsearch & pyparsing
# stuff from twill3/included-packages/.  NOTE: this works with eggs! hooray!
#

import sys, os.path
thisdir = os.path.dirname(__file__)

# add extensions directory at the *end* of sys.path.  This means that
# user extensions will take priority over twill3 extensions.
extensions = os.path.join(thisdir, 'extensions')
sys.path.append(extensions)

# add other_packages in at the *beginning*, so that the correct
# (patched) versions of pyparsing and mechanize get imported.
wwwsearchlib = os.path.join(thisdir, 'other_packages')
sys.path.insert(0, wwwsearchlib)

# the two core components of twill3:
from .shell import TwillCommandLoop
from .parse import execute_file, execute_string

# convenience function or two...
from .commands import get_browser

def get_browser_state():
    import warnings
    warnings.warn("""\
get_browser_state is deprecated; use 'twill3.get_browser() instead.
""", DeprecationWarning)
    return get_browser()

# initialize global dict
from . import namespaces
namespaces.init_global_dict()

from .wsgi_intercept import add_wsgi_intercept, remove_wsgi_intercept

def set_output(fp):
    """
    Have standard output from twill3 go to the given fp instead of
    stdout.  fp=None will reset to stdout.
    """
    from . import commands, browser
    commands.OUT = browser.OUT = fp

def set_errout(fp):
    """
    Have error output from twill3 go to the given fp instead of stderr.
    fp=None will reset to stderr.
    """
    from . import commands
    if fp:
        commands.ERR = fp
    else:
        commands.ERR = sys.stderr
