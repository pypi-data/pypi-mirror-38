class EmptyAcceptedParameterException(Exception):
    """An Exception raised when there are no parameters for an AcceptedParameter object.
    """
    pass

class EmptyCommandException(Exception):
    """An Exception raised when there are no parameters for a Command object.
    """
    pass

class EmptyErrorException(Exception):
    """An Exception raised when there are no parameters for an Error object.
    """
    pass

class EmptyParameterException(Exception):
    """An Exception raised when there are no parameters for a Parameter object.
    """
    pass

class NoSuchAcceptedParameterException(Exception):
    """An Exception raised when there is no AcceptedParameter object specified by an identifier.
    """
    pass

class NoSuchErrorException(Exception):
    """An Exception raised when there is no Error object specified by an identifier.
    """
    pass

class NoSuchParameterException(Exception):
    """An Exception raised when there is no Parameter object specified by an identifier.
    """
    pass