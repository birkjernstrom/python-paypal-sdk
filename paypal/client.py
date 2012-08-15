# -*- coding: utf-8 -*-
"""
"""

import uuid
import urllib2

from paypal import util, service, exceptions

API_VERSION = '93.0'

SANDBOX_3TOKEN_ENDPOINT = 'https://api-3t.sandbox.paypal.com/nvp'
PRODUCTION_3TOKEN_ENDPOINT = 'https://api-3t.paypal.com/nvp'

PAYPAL_URL = 'https://www.paypal.com'
PAYPAL_SANDBOX_URL = 'https://www.sandbox.paypal.com'

TYPE_MODULE_MAPPING = {
    'ExpressCheckout': service.express_checkout,
}


class Config(object):
    """
    """
    def __init__(self,
                 api_username,
                 api_password,
                 api_signature,
                 application_id,
                 validate_requests=True,
                 validate_responses=False,
                 log_group_id=False,
                 sandbox=True):
        """
        """
        self.api_username = api_username
        self.api_password = api_password
        self.api_signature = api_signature
        self.application_id = application_id
        self.validate_requests = validate_requests
        self.validate_responses = validate_responses
        self.log_group_id = log_group_id
        self.is_sandbox = sandbox

    @property
    def endpoint(self):
        if self.is_sandbox:
            return SANDBOX_3TOKEN_ENDPOINT
        return PRODUCTION_3TOKEN_ENDPOINT


class BaseClient(object):
    def __init__(self, api_service, config=None, **kwargs):
        if not isinstance(config, Config):
            config = Config(**kwargs)

        self.config = config
        self.api_service = api_service
        self.type_module = TYPE_MODULE_MAPPING[api_service]

    def get_type_classname(self, method, is_request=True):
        to_append = ('Response', 'Request')[is_request]
        return '%s%s' % (method, to_append)

    def get_type(self, method, is_request=True):
        classname = self.get_type_classname(method, is_request=is_request)
        return getattr(self.type_module, classname)

    def normalize_request(self, request):
        request.version = API_VERSION
        request.user = self.config.api_username
        request.pwd = self.config.api_password
        request.signature = self.config.api_signature
        return request

    def generate_group_id(self):
        # Generate unique API request/response group identifier in case
        # permitted in the client configuration. The identifier is logged
        # along with both the request and response. This can be useful in
        # scenarios where the request and response records are not guaranteed
        # to be written sequentially - for instance in case a asynchronous
        # PayPal client is being used. Thus easing the search for the
        # response of an API request and vice versa.
        group_id = uuid.uuid4().hex if self.config.log_group_id else None
        return group_id

    def generate_request(self, method, payload):
        request_cls = self.get_type(method, is_request=True)
        request = request_cls(**payload)
        request = self.normalize_request(request)
        if self.config.validate_requests and not request.validate():
            raise exceptions.InvalidRequestException()

        return request

    def generate_response(self, method, raw_response, as_dict=False):
        response_cls = self.get_type(method, is_request=False)
        decoded_response = response_cls.decode(raw_response)
        if as_dict:
            return decoded_response

        response = response_cls(**decoded_response)
        if self.config.validate_responses and not response.validate():
            raise exceptions.InvalidResponseException()

        return response

    def get_headers(self):
        return {}
        #h['X-PAYPAL-REQUEST-DATA-FORMAT'] = 'NV'
        #h['X-PAYPAL-RESPONSE-DATA-FORMAT'] = 'NV'
        #h['X-PAYPAL-SECURITY-USERID'] = self.config.api_username
        #h['X-PAYPAL-SECURITY-PASSWORD'] = self.config.api_password
        #h['X-PAYPAL-SECURITY-SIGNATURE'] = self.config.api_signature
        #h['X-PAYPAL-APPLICATION-ID'] = self.config.application_id
        #return h

    def generate_paypal_url(self, path):
        base = PAYPAL_SANDBOX_URL
        if not self.config.is_sandbox:
            base = PAYPAL_URL
        return base + path

    def execute(self,
                method,
                endpoint,
                headers,
                body,
                response_as_dict=False,
                group_id=None):
        try:
            request = urllib2.Request(endpoint, body, headers)
            encoded = urllib2.urlopen(request).read()
            response = self.generate_response(method, encoded,
                                              as_dict=response_as_dict)

            self.log_api_response(encoded, response, group_id=group_id)
            return response
        except urllib2.HTTPError as e:
            util.api_logger.error(e.strerror)
        return None

    def log_api_request(self, encoded, decoded, group_id=None):
        if group_id is not None:
            message = '(GID %s) Request: %s => %s'
            util.api_logger(message, group_id, decoded, encoded)
        else:
            util.api_logger('Request: %s => %s', decoded, encoded)

    def log_api_response(self, encoded, decoded, group_id=None):
        params, messages = []
        if group_id is not None:
            messages.append('(GID %s)')
            params.append(group_id)

        correlation_id = decoded.correlationid
        if correlation_id:
            messages.append('Response: [%s]: %s => %s')
            params.extend((correlation_id, encoded, decoded))
        else:
            messages.append('Response: %s => %s')
            params.extend((encoded, decoded))

        message = ' '.join(messages)
        util.api_logger(message, *params)

    def __call__(self,
                 method,
                 endpoint=None,
                 payload=None,
                 response_as_dict=False,
                 **params):
        """
        """
        endpoint = endpoint if endpoint else self.config.endpoint
        if payload is not None:
            params.update(payload)

        headers = self.get_headers()
        request = self.generate_request(method, params)
        encoded_request = request.encode()
        group_id = self.generate_group_id()

        self.log_api_request(encoded_request, request, group_id=group_id)


class Client(BaseClient):
    pass
