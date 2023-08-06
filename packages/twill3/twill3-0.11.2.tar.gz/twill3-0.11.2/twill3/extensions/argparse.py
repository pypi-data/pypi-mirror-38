"""
Extension functions for parsing sys.argv.

Commands:

   get_args -- load all command-line arguments after the last --
      into $arg1...$argN.
   
"""

import twill3.utils

def get_args(require=0):
    """
    >> get_args [<require>]

    Load the command line arguments after the last '--' into $arg1...$argN,
    optionally requiring at least 'require' such arguments.
    """
    from twill3 import commands, namespaces, shell, errors

    global_dict, local_dict = namespaces.get_twill_glocals()

    require = int(require)

    if len(shell.twillargs) < require:
        from twill3.errors import TwillAssertionError
        raise TwillAssertionError("too few arguments; %d rather than %d" % \
                                    (len(shell.twillargs), require,))

    if shell.twillargs:
        for i, arg in enumerate(shell.twillargs):
            global_dict["arg%d" % (i + 1,)] = arg

        print("get_args: loaded %d args as $arg1..$arg%d." % \
                             (i + 1, i + 1), file=commands.OUT)
    else:
        print("no arguments to parse!", file=commands.OUT)
