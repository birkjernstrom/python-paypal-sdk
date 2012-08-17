# -*- coding: utf-8 -*-

import nvp


class Request(dict):
    NVP_CONVENTION = 'bracket'
    KEY_ENCODING_FILTER = None

    def encode(self):
        return nvp.dumps(
            self, convention=self.NVP_CONVENTION,
            key_filter=self.KEY_ENCODING_FILTER,
        )


class Response(dict):
    NVP_CONVENTION = 'bracket'
    KEY_DECODING_FILTER = None

    @classmethod
    def decode(cls, encoded_response):
        return nvp.loads(
            encoded_response, cls.NVP_CONVENTION,
            key_filter=cls.KEY_DECODING_FILTER,
        )

    @classmethod
    def get_decoded_instance(cls, encoded_response):
        return cls(cls.decode(encoded_response))


class UnderscoreConventionRequest(Request):
    NVP_CONVENTION = 'underscore'

    def encode(self):
        return nvp.dumps(
            self, convention=self.NVP_CONVENTION,
            key_filter=lambda key: key.upper(),
        )


class UnderscoreConventionResponse(Response):
    NVP_CONVENTION = 'underscore'

    @classmethod
    def decode(cls, encoded_response):
        return nvp.loads(encoded_response, key_filter=lambda key: key.lower())
