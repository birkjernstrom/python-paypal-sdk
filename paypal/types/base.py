# -*- coding: utf-8 -*-
"""

"""

CLS_FIELDS_ATTRIBUTE = '__fields__'
CLS_REQUIRED_FIELDS_ATTRIBUTE = '__required_fields__'


def get_fields(obj):
    return getattr(obj, CLS_FIELDS_ATTRIBUTE, {}).copy()


def get_field_inheritance(bases):
    fields = {}
    for base in bases:
        to_set = get_fields(base)
        if to_set:
            fields.update(to_set)
    return fields


class TypeConstructor(type):
    def __new__(cls, name, bases, attributes):
        new = super(TypeConstructor, cls).__new__
        ret = new(cls, name, bases, attributes)

        parents = [b for b in bases if isinstance(b, TypeConstructor)]
        if not parents:
            return ret

        required = {}
        reserved_attributes = dir(BaseType)
        fields = get_field_inheritance(bases)

        for name, field in fields.iteritems():
            if not isinstance(field, Field):
                continue

            if name in reserved_attributes or name.startswith('_'):
                message = 'Illegal field name: %s %s'
                raise AttributeError(message % (name, repr(ret)))

            field.__bind__(name, ret)
            if field.is_required():
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


class Field(object):
    def __init__(self,
                 name=None,
                 required=None,
                 choices=(),
                 default=None):
        """
        """
        self.name = name
        self.is_required = required
        self.choices = choices
        self.default = default
        self.initialize()

    def initialize(self):
        pass

    def get_default(self):
        return self.default

    def is_required(self):
        return False

    def get_attribute_name(self):
        """Retrieve attribute key for instance property."""
        return '_field_%s' % self.name

    def sanitize(self, value):
        return value

    def validate(self, value):
        return True

    def __bind__(self, key, owner):
        self.owner_cls = owner
        self.owner_name = key
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

        if not is_none or self.is_required:
            if not self.validate(value):
                raise_validation_exception(field_name, value)

            local_func_name = 'validate_field_%s' % field_name
            local_validation = getattr(instance, local_func_name, None)
            if local_validation and not local_validation(value):
                raise_validation_exception(field_name, value)

        attribute = self.get_attribute_name()
        setattr(instance, attribute, value)


def to_dict(obj):
    pass
