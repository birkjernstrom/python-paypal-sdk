# -*- coding: utf-8 -*-
"""PayPal package specific exceptions."""


class BaseException(Exception):
    """PayPal Base Exception."""


class InvalidRequestException(BaseException):
    """Exception corresponding to invalid API request parameters."""


class InvalidResponseException(BaseException):
    """Exception corresponding to invalid API response parameters."""
