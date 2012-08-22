# -*- coding: utf-8 -*-

import nvp


class Request(dict):
    NVP_CONVENTION = 'bracket'

    @staticmethod
    def encode_value_filter(value):
        if hasattr(value, 'encode'):
            value = value.encode('utf-8')
        return value

    def encode(self):
        return nvp.dumps(self, convention=self.NVP_CONVENTION,
                         value_filter=self.encode_value_filter)


class Response(dict):
    NVP_CONVENTION = 'bracket'

    @staticmethod
    def decode_value_filter(value):
        if hasattr(value, 'decode'):
            value = value.decode('utf-8')
        return value

    @classmethod
    def decode(cls, encoded_response):
        return nvp.loads(encoded_response,
                         value_filter=cls.decode_value_filter)

    @classmethod
    def get_decoded_instance(cls, encoded_response):
        return cls(cls.decode(encoded_response))


class UnderscoreConventionRequest(Request):
    NVP_CONVENTION = 'underscore'

    def encode(self):
        return nvp.dumps(
            self, convention=self.NVP_CONVENTION,
            key_filter=lambda key: key.upper(),
            value_filter=self.encode_value_filter,
        )


class UnderscoreConventionResponse(Response):
    NVP_CONVENTION = 'underscore'

    @classmethod
    def decode(cls, encoded_response):
        return nvp.loads(encoded_response,
                         key_filter=lambda key: key.lower(),
                         value_filter=cls.decode_value_filter)
