from zope.interface import Interface
from zope.interface.common.interfaces import IAttributeError
from zope.interface.common.interfaces import IException


class ISerializableException(IException):
    """
    An exception that can be deserialized
    """

    def json_data():
        """
        return json serializable data to be used
        with exception data in responses
        """


class IUnauthorized(IException):
    '''
    '''


class IForbidden(IException):
    '''
    '''


class IForbiddenAttribute(IForbidden, IAttributeError):
    '''
    '''


class IErrorResponseException(Interface):
    '''
    Provide response object for uncaught exceptions
    '''
