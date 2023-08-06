"""
Exception signaling that something went wrong while calling the API.
Future version of this package will add more specific exceptions,
but all will inherit from this one, so it's safe to test against it.
"""


class EnlOneException(Exception):
    """
    Exception signaling that something went wrong while calling the API.
    Future version of this package will add more specific exceptions,
    but all will inherit from this one, so it's safe to test against it.
    """
    pass


class NotImplementedByBackendException(EnlOneException):
    """
    Raised by placeholder method still not implemeted by the backend.
    """
    pass


class PyEnlOneNotImplementedException(EnlOneException):
    """
    Raised by placeholder method still not implemeted by the backend.
    """
    pass
