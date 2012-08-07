# -*- coding: utf-8 -*-

__all__ = [
    'BaseType', 'Field',
    'get_fields', 'get_field_inheritance',
]

from paypal.types import base

BaseType = base.BaseType
Field = base.Field


get_fields = base.get_fields
get_field_inheritance = base.get_field_inheritance
