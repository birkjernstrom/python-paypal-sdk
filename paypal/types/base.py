# -*- coding: utf-8 -*-
"""

"""

import decimal

from paypal.util import ensure_unicode


CLS_FIELDS_ATTRIBUTE = '__fields__'
CLS_REQUIRED_FIELDS_ATTRIBUTE = '__required_fields__'


def get_fields(obj):
    return getattr(obj, CLS_FIELDS_ATTRIBUTE, {})


def get_field_inheritance(bases):
    fields = {}
    for base in bases:
        to_set = get_fields(base)
        if to_set:
            fields.update(to_set)
    return fields


def is_dict(obj):
    return hasattr(obj, '__getitem__') and hasattr(obj, 'setdefault')


def is_non_string_sequence(obj):
    return hasattr(obj, '__iter__') and not is_dict(obj)


###############################################################################
# CORE TYPE CLASSES
###############################################################################


class TypeConstructor(type):
    def __new__(cls, name, bases, attributes):
        constructor = super(TypeConstructor, cls).__new__
        ret = constructor(cls, name, bases, attributes)

        parents = [b for b in bases if isinstance(b, TypeConstructor)]
        if not parents:
            return ret

        reserved_attributes = dir(BaseType)
        fields = get_field_inheritance(bases)

        required = {}
        for name, field in attributes.iteritems():
            if not isinstance(field, Field):
                continue

            if name in reserved_attributes or name.startswith('_'):
                message = 'Illegal field name: %s %s'
                raise AttributeError(message % (name, repr(ret)))

            field.__bind__(ret, name)
            if field.required:
                required[name] = field
            fields[name] = field

        setattr(ret, CLS_FIELDS_ATTRIBUTE, fields)
        setattr(ret, CLS_REQUIRED_FIELDS_ATTRIBUTE, required)
        return ret

    def get_param_name(self):
        name = self.__class__.__name__
        if name.endswith('Type'):
            name = name[:-4]
        return name.lower()


class BaseType(object):
    __metaclass__ = TypeConstructor

    @classmethod
    def get_fields(cls):
        return getattr(cls, CLS_FIELDS_ATTRIBUTE)

    @classmethod
    def get_required_fields(cls):
        return getattr(cls, CLS_REQUIRED_FIELDS_ATTRIBUTE)

    def __init__(self, *args, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    def validate(self):
        pass

    def to_dict(self):
        ret = {}
        print 'RUN %s.to_dict()' % (self)
        fields = self.get_fields()
        for name, field in fields.iteritems():
            value = getattr(self, name)
            if not field.is_empty(value):
                ret[name] = field.to_dict(value)
        return ret


###############################################################################
# FIELDS
###############################################################################

class Field(object):
    def __init__(self,
                 name=None,
                 required=False,
                 choices=(),
                 default=None,
                 **kwargs):
        """
        """
        self.name = name
        self.required = required
        self.choices = choices
        self.default = default
        self.initialize(**kwargs)

    def initialize(self):
        pass

    def get_default(self):
        return self.default

    def get_attribute_name(self):
        """Retrieve attribute key for instance property."""
        return '_field_%s' % self.name

    def sanitize(self, value):
        return value

    def is_empty(self, value):
        return (value is None)

    def validate(self, value):
        if self.is_empty(value) and self.required:
            message = 'Field %s cannot be an empty value since it is required'
            raise ValueError(message % (self.name))

        if self.choices:
            match = False
            for choice in self.choices:
                if choice == value:
                    match = True
                    break

            if not match:
                message = 'Given value is not one of the accepted choices: %s'
                raise ValueError(message % value)

        return True

    def to_dict(self, value):
        return value

    def __bind__(self, owner, key):
        self.owner = owner
        if self.name is None:
            self.name = key

    def __get__(self, instance, owner):
        if instance is None:
            return self

        try:
            attribute = self.get_attribute_name()
            return getattr(instance, attribute)
        except AttributeError:
            # Lazy-load instance attribute
            value = self.get_default()
            setattr(instance, attribute, value)
            return value

    def __set__(self, instance, value):
        if instance is None:
            return self

        field_name = self.name
        is_none = (value is None)
        if not is_none:
            value = self.sanitize(value)
            local_func_name = 'sanitize_field_%s' % field_name
            local_sanitization = getattr(instance, local_func_name, None)
            if local_sanitization:
                value = local_sanitization(value)

        def raise_validation_exception(name, value):
            message = 'Invalid value given for field %s: %s'
            raise ValueError(message % (field_name, value))

        if not is_none or self.required:
            if not self.validate(value):
                raise_validation_exception(field_name, value)

            local_func_name = 'validate_field_%s' % field_name
            local_validation = getattr(instance, local_func_name, None)
            if local_validation and not local_validation(value):
                raise_validation_exception(field_name, value)

        attribute = self.get_attribute_name()
        setattr(instance, attribute, value)


class UnicodeField(Field):
    def initialize(self,
                   min_length=None,
                   max_length=None,
                   length=None):
        self.min_length = min_length
        self.max_length = max_length
        if length is not None:
            self.min_length = length
            self.max_length = length

    def sanitize(self, value):
        return ensure_unicode(str(value))

    def validate(self, value):
        if not super(UnicodeField, self).validate(value):
            return False

        value_len = len(value)
        if self.min_length is not None and value_len < self.min_length:
            message = 'Given value is less than %s: %s'
            raise ValueError(message % (self.min_length, value))

        if self.max_length is not None and value_len > self.max_length:
            message = 'Given value is greater than %s: %s'
            raise ValueError(message % (self.max_length, value))

        return True


class StringField(UnicodeField):
    """Field intended for unicode string values."""


class NumericField(Field):
    def initialize(self,
                   min=None,
                   max=None,
                   unsigned=False):
        self.min = min
        self.max = max
        self.unsigned = unsigned

    def validate(self, value):
        if not super(NumericField, self).validate(value):
            return False

        if self.unsigned and value < 0:
            message = 'Given value is not unsigned: %s'
            raise ValueError(message % value)

        if self.min is not None and value < self.min:
            message = 'Given value is less than %s: %s'
            raise ValueError(message % (self.min, value))

        if self.max is not None and value > self.max:
            message = 'Given value is greater than %s: %s'
            raise ValueError(message % (self.max, value))

        return True


class IntegerField(NumericField):
    def sanitize(self, value):
        return int(value)


class BooleanField(Field):
    def sanitize(self, value):
        try:
            # In PayPal responses boolean values are represented as integers.
            # Therefore, we type cast the value to an integer prior to
            # to converting it to a boolean.
            # In order to avoid '0' values being represented as True.
            value = int(value)
        except ValueError:
            pass
        return bool(value)

    def to_dict(self, value):
        return 1 if value else 0


class TypeField(Field):
    def __init__(self,
                 name=None,
                 required=None,
                 instanceof=BaseType):
        """
        """
        super(TypeField, self).__init__(name=name, required=required)
        self.instanceof = instanceof

    def sanitize(self, value):
        value = super(TypeField, self).sanitize(value)
        if is_dict(value):
            value = self.instanceof(**value)
        return value

    def validate(self, obj):
        if isinstance(obj, self.instanceof):
            return True

        message = 'Given field value is not an instance of type %s'
        raise ValueError(message % self.instanceof)

    def to_dict(self, obj):
        return obj.to_dict()


class ListTypeField(Field):
    def __init__(self,
                 name=None,
                 required=None,
                 instanceof=BaseType):
        super(ListTypeField, self).__init__(name=name, required=required)
        self.instanceof = instanceof

    def sanitize(self, value):
        value = super(ListTypeField, self).sanitize(value)
        if isinstance(value, self.instanceof):
            return value

        # Return value in case it is not a list, tuple, set or frozenset
        if not is_non_string_sequence(value):
            return value

        return [self.instanceof(**current) for current in value]

    def validate(self, sequence):
        if not super(ListTypeField, self).validate(sequence):
            return False

        if not is_non_string_sequence(sequence):
            msg = 'Invalid value given. Expected list of instances of type. %s'
            raise ValueError(msg % self.instanceof)

        for instance in sequence:
            if not isinstance(instance, self.instanceof):
                msg = 'Invalid instance given. Expected one of class %s.'
                raise ValueError(msg % self.instanceof)

            # Trigger validation for each instance
            instance.validate()

        return True

    def to_dict(self, sequence):
        return [instance.to_dict() for instance in sequence]


class ListField(Field):
    def __init__(self,
                 name=None,
                 required=None,
                 sanitization_callback=None,
                 validation_callback=None):
        super(ListField, self).__init__(name=name, required=required)
        self.sanitization_callback = sanitization_callback
        self.validation_callback = validation_callback

    def sanitize(self, value):
        value = super(ListField, self).sanitize(value)
        if self.sanitization_callback:
            return self.sanitization_callback(value)
        return value

    def validate(self, value):
        if not super(ListField, self).validate(value):
            return False

        if self.validation_callback:
            return self.validation_callback(value)
        return True


class ConstantField(Field):
    def __init__(self, constant, name=None):
        super(ConstantField, self).__init__(name=name)
        attribute = self.get_attribute_name()
        setattr(self, attribute, constant)

    def __set__(self, instance, value):
        if instance is None:
            return self

        message = 'Cannot set value for field of type constant: %s'
        raise RuntimeError(message % value)


class URLField(UnicodeField):
    def sanitize(self, value):
        if not (value.startswith('http://') or value.startswith('https://')):
            value = 'http://%s' % value
        return value


###############################################################################
# MONETARY FIELDS
###############################################################################

#: We set all the traps possible that will not cause unnecessary
#: exceptions. The reason for this is because we want to make
#: it as strict as possible. It is crucial that no unintended
#: exception is silent.
CONTEXT_TRAPS = [decimal.Clamped,
                 decimal.DecimalException,
                 decimal.DivisionByZero,
                 decimal.InvalidOperation,
                 decimal.Overflow,
                 decimal.Underflow]

#: The decimal context utilized in our handling of monetary
#: decimals. The default context is not optimal since
#: it can be changed within the thread and by design does
#: not raise all arithmetic exceptions which is crucial
#: when dealing with such sensitive data as money.
CONTEXT = decimal.Context(prec=28,
                          rounding=decimal.ROUND_HALF_UP,
                          traps=CONTEXT_TRAPS)

decimal.setcontext(CONTEXT)

#: Traps to set for context used when executing quantize.
#: Quantize unlike other methods will raise InvalidOperation
#: in case the precision of the coefficient is larger than the
#: precision of the context. Something we can accept in those rare
#: circumstances.
CONTEXT_QUANTIZE_TRAPS = CONTEXT_TRAPS[:]
CONTEXT_QUANTIZE_TRAPS.remove(decimal.InvalidOperation)

#: Context to be utilized during execution of the quantize decimal method.
CONTEXT_QUANTIZE = decimal.Context(prec=CONTEXT.prec,
                                   rounding=CONTEXT.rounding,
                                   traps=CONTEXT_QUANTIZE_TRAPS)


def get_as_decimal(value):
    """Retrieve given value as a decimal instance with correct context.

    :param value: The value to convert into a decimal
    """
    if isinstance(value, decimal.Decimal):
        return value
    return CONTEXT.create_decimal(str(value))


class Money(object):
    def __init__(self, amount, precision=2):
        self.amount = get_as_decimal(amount)
        self.precision = precision

    def __repr__(self):
        return 'Money(%s)' % (str(self.get_quantized()))

    def __str__(self):
        return str(self.get_quantized())

    def get_quantized(self):
        """Retrieve the quantized value."""
        quantize_by = '1.%s' % ('0' * self.precision)
        quantize_by = get_as_decimal(quantize_by)
        return self.amount.quantize(quantize_by, context=CONTEXT_QUANTIZE)

    # Unary plus
    def __pos__(self):
        return type(self)(self.amount)

    # Unary minus
    def __neg__(self):
        return type(self)(self.amount * -1)

    # Addition
    def __add__(self, amount):
        amount = get_as_decimal(amount)
        return type(self)(self.amount + amount)

    def __sub__(self, amount):
        amount = get_as_decimal(amount)
        return type(self)(self.amount - amount)

    def __mul__(self, amount):
        amount = get_as_decimal(amount)
        return type(self)(self.amount * amount)

    def __div__(self, amount):
        amount = get_as_decimal(amount)
        return type(self)(self.amount / amount)

    def __rdiv__(self, amount):
        amount = get_as_decimal(amount)
        return type(self)(amount / self.amount)

    def __rmod__(self, amount):
        amount = get_as_decimal(amount)
        return type(self)((self.amount * amount) / 100)

    def __float__(self):
        return self.amount.__float__()

    __radd__ = __add__
    __rsub__ = __sub__
    __rmul__ = __mul__

    def __eq__(self, amount):
        if amount is None:
            return False

        amount = get_as_decimal(amount)
        return self.amount == amount

    def __ne__(self, amount):
        return not self.__eq__(amount)

    def __lt__(self, amount):
        amount = get_as_decimal(amount)
        return self.amount < amount

    def __gt__(self, amount):
        amount = get_as_decimal(amount)
        return self.amount > amount

    def __le__(self, other):
        return self < other or self == other

    def __ge__(self, other):
        return self > other or self == other


class MoneyField(NumericField):
    def initialize(self,
                   min=None,
                   max=None,
                   unsigned=False,
                   precision=2):
        self.min = Money(min, precision=precision) if min else None
        self.max = Money(max, precision=precision) if max else None
        self.unsigned = unsigned
        self.precision = 2

        if self.default:
            self.default = Money(self.default, precision=precision)

    def sanitize(self, value):
        return Money(value, precision=self.precision)
