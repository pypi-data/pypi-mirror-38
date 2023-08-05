from enum import Enum


class ErrorHandler(Enum):
    PASS_AS_VARIABLE = 1
    RAISE = 2
    CUSTOM = 3


class FailureReason(Enum):
    NOT_LOGGED_IN = 1
    MISSING_PERMISSION = 2
    MISSING_ROLE = 3
    INTERNAL_FAILURE = 4
