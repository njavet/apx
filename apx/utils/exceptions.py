
class ActivityProcessingError(Exception):
    """Base exception for activity processing errors."""


class ActivityProcessingWarning(Exception):
    """Raised when the input seems not correct."""


class InvalidActivityError(ActivityProcessingError):
    """Raised when the input activity is invalid."""


class DatabaseError(ActivityProcessingError):
    """Raised for database-related errors."""
