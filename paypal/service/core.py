# -*- coding: utf-8 -*-

import nvp
from paypal import util


def _utf8(value):
    value = util.ensure_unicode(value)
    if hasattr(value, 'encode'):
        return value.encode('utf-8')
    return value


class Request(dict):
    NVP_CONVENTION = 'bracket'

    def encode(self, convention=None):
        convention = convention if convention else self.NVP_CONVENTION
        return nvp.dumps(util.ensure_unicode(self),
                         key_filter=self.encode_key_filter,
                         value_filter=self.encode_value_filter,
                         convention=convention)

    def encode_key_filter(self, key):
        return _utf8(key)

    def encode_value_filter(self, value):
        return _utf8(value)


class Response(dict):
    @classmethod
    def decode(cls, encoded_response):
        return nvp.loads(encoded_response,
                         key_filter=cls.decode_key_filter,
                         value_filter=cls.decode_value_filter)

    @classmethod
    def get_decoded_instance(cls, encoded_response):
        return cls(cls.decode(encoded_response))

    @staticmethod
    def decode_key_filter(key):
        return util.ensure_unicode(key)

    @staticmethod
    def decode_value_filter(value):
        return util.ensure_unicode(value)


class UnderscoreConventionRequest(Request):
    NVP_CONVENTION = 'underscore'

    def encode_key_filter(self, key):
        parent = super(UnderscoreConventionRequest, self).encode_key_filter
        return parent(key.lower())


class UnderscoreConventionResponse(Response):
    @staticmethod
    def decode_key_filter(key):
        return util.ensure_unicode(key.lower())
