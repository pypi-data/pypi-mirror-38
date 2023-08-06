class TwillException(Exception):
    """
    General twill3 exception.
    """
    pass

class TwillAssertionError(TwillException):
    """
    AssertionError to raise upon failure of some twill3 command.
    """
    pass

class TwillNameError(TwillException):
    """
    Error to raise when an unknown command is called.
    """
    pass
