# -*- coding: utf-8 -*-

__all__ = [
    'BaseType', 'Money', 'Field', 'UnicodeField',
    'StringField', 'IntegerField', 'BooleanField',
    'TypeField', 'ListTypeField', 'ListField',
    'ConstantField', 'MoneyField',

    'gen_strlen_validator', 'gen_unsigned_int_validator',
    'gen_choice_validator', 'get_fields', 'get_field_inheritance',

    'express_checkout',
]

from paypal.types import core, express_checkout

###############################################################################
# ALIASES
###############################################################################

#----------------------------------------
# Validator Generator Aliases
#----------------------------------------

#: Alias for ``core.gen_strlen_validator``
gen_strlen_validator = core.gen_strlen_validator
#: Alias for ``core.gen_unsigned_int_validator``
gen_unsigned_int_validator = core.gen_unsigned_int_validator
#: Alias for ``core.gen_choice_validator``
gen_choice_validator = core.gen_choice_validator

#----------------------------------------
# Type Aliases
#----------------------------------------

#: Alias for ``core.BaseType``
BaseType = core.BaseType
#: Alias for ``core.Money``
Money = core.Money

#----------------------------------------
# Field Aliases
#----------------------------------------

#: Alias for ``core.Field``
Field = core.Field
#: Alias for ``core.UnicodeField``
UnicodeField = core.UnicodeField
#: Alias for ``core.StringField``
StringField = core.StringField
#: Alias for ``core.IntegerField``
IntegerField = core.IntegerField
#: Alias for ``core.BooleanField``
BooleanField = core.BooleanField
#: Alias for ``core.TypeField``
TypeField = core.TypeField
#: Alias for ``core.ListTypeField``
ListTypeField = core.ListTypeField
#: Alias for ``core.ConstantField``
ConstantField = core.ConstantField
#: Alias for ``core.MoneyField``
MoneyField = core.MoneyField

#----------------------------------------
# Function Aliases
#----------------------------------------

#: Alias for ``core.get_fields``
get_fields = core.get_fields
#: Alias for ``core.get_field_inheritance``
get_field_inheritance = core.get_field_inheritance
