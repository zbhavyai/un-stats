# File:        custom_errors.py
# Authors:     Bhavyai Gupta, Brandon Attai
# Description: Source Code for creating custom exceptions


class ValueOutOfRange(Exception):
    """Raised when user input is out of range"""
    pass


class ValueDuplicate(Exception):
    """Raised when user repeated their input when unique values were required"""
    pass
