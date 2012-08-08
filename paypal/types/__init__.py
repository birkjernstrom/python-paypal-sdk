# -*- coding: utf-8 -*-

__all__ = [
    'BaseType', 'Money', 'Field', 'UnicodeField',
    'StringField', 'IntegerField', 'BooleanField',
    'TypeField', 'ConstantField', 'MoneyField',
    'get_fields', 'get_field_inheritance',
]

from paypal.types import base

BaseType = base.BaseType
Money = base.Money

# Field aliases
Field = base.Field
UnicodeField = base.UnicodeField
StringField = base.StringField
IntegerField = base.IntegerField
BooleanField = base.BooleanField
TypeField = base.TypeField
ConstantField = base.ConstantField
MoneyField = base.MoneyField


get_fields = base.get_fields
get_field_inheritance = base.get_field_inheritance
