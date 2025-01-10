from enum import IntEnum


class ErrorCodes(IntEnum):
    OK = 0  # Success
    ERR_UNEXPECTED = -1  # Unexpected failure
    ERR_NOTIMPL = -2  # Not implemented
    ERR_OUTOFMEMORY = -3  # Out of memory
    ERR_INVALIDARG = -4  # Invalid argument
    ERR_NOINTERFACE = -5  # No such interface supported
    ERR_POINTER = -6  # Pointer error
    ERR_HANDLE = -7  # Handle error
    ERR_ABORT = -8  # Operation aborted
    ERR_FAIL = -9  # Unspecified failure
    ERR_ACCESSDENIED = -10  # Access denied
