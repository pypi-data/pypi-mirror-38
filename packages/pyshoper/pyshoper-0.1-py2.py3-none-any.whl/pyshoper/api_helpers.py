class ShoperApiError(Exception):
    """Base class for shoper api exceptions"""
    pass


class InvalidRequest(ShoperApiError):
    """Raised when invalid request"""
    pass


class InvalidRequestInsufficientPermissions(ShoperApiError):
    """Raised when invalid request - insufficient permissions"""
    pass


class InvalidRequestInvalidAuthenticationMethod(ShoperApiError):
    """Raised when invalid request - invalid authentication method"""
    pass


class AuthenticationError(ShoperApiError):
    """Raised when authentication error"""
    pass


class PaymentRequiredError(ShoperApiError):
    """Raised when payment required"""
    pass


class AccessDeniedError(ShoperApiError):
    """Raised when access denied """
    pass


class ObjectNotExistError(ShoperApiError):
    """Raised when an object doesn't exist"""
    pass


class InvalidRequestMethodError(ShoperApiError):
    """Raised when invalid request method"""
    pass


class AdministratorLockConflictError(ShoperApiError):
    """Raised when conflict - another administrator has locked an access to the object"""
    pass


class CallsLimitExceededError(ShoperApiError):
    """Raised when calls limit exceeded"""
    pass


class ApplicationError(ShoperApiError):
    """Raised when application error"""
    pass


class MethodNotImplementedError(ShoperApiError):
    """Raised when method not implemented"""
    pass


class ApplicationLockError(ShoperApiError):
    """Raised when system is temporarily unavailable (application has been completely locked by administrator)"""
    pass


error_map = {
    (400, 'invalid_request'): InvalidRequest,
    (400, 'invalid_scope'): InvalidRequestInsufficientPermissions,
    (400, 'invalid_grant'): InvalidRequestInvalidAuthenticationMethod,
    (401, 'unauthorized_client'): AuthenticationError,
    (402, 'access_denied'): PaymentRequiredError,
    (403, 'insufficient_scope'): AccessDeniedError,
    (404, 'server_error'): ObjectNotExistError,
    (405, 'invalid_request'): InvalidRequestMethodError,
    (409, 'server_error'): AdministratorLockConflictError,
    (429, 'temporarily_unavailable'): CallsLimitExceededError,
    (500, 'server_error'): ApplicationError,
    (501, 'server_error'): MethodNotImplementedError,
    (503, 'temporarily_unavailable'): ApplicationLockError,
}
