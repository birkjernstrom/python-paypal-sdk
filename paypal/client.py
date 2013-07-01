# -*- coding: utf-8 -*-
"""
"""

import uuid
import urllib2

from paypal import util, service

###############################################################################
# CONSTANTS
###############################################################################

API_VERSION = '93.0'

SANDBOX_3TOKEN_ENDPOINT = 'https://api-3t.sandbox.paypal.com/nvp'
PRODUCTION_3TOKEN_ENDPOINT = 'https://api-3t.paypal.com/nvp'

PAYPAL_URL = 'https://www.paypal.com'
PAYPAL_SANDBOX_URL = 'https://www.sandbox.paypal.com'

TYPE_MAPPING = {
    'ExpressCheckout': (
        service.ExpressCheckoutRequest,
        service.ExpressCheckoutResponse,
    ),
}


###############################################################################
# CLIENT CONFIGURATION
###############################################################################

class Config(object):
    """
    """
    def __init__(self,
                 api_username,
                 api_password,
                 api_signature,
                 application_id,
                 log_group_id=False,
                 sandbox=True):
        """
        """
        self.api_username = api_username
        self.api_password = api_password
        self.api_signature = api_signature
        self.application_id = application_id
        self.log_group_id = log_group_id
        self.is_sandbox = sandbox

    @property
    def endpoint(self):
        if self.is_sandbox:
            return SANDBOX_3TOKEN_ENDPOINT
        return PRODUCTION_3TOKEN_ENDPOINT


###############################################################################
# CLIENTS
###############################################################################

class BaseClient(object):

    http_timeout = 10  # Timeout in seconds, passed to urllib2.urlopen

    def __init__(self, api_service, config=None, **kwargs):
        if not isinstance(config, Config):
            config = Config(**kwargs)

        request_cls, response_cls = TYPE_MAPPING[api_service]

        self.config = config
        self.api_service = api_service
        self.request_cls = request_cls
        self.response_cls = response_cls

    def normalize_request(self, request, method):
        request.update({
            'version': API_VERSION,
            'user': self.config.api_username,
            'pwd': self.config.api_password,
            'signature': self.config.api_signature,
            'method': method,
        })

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
        request = self.request_cls(payload)
        self.normalize_request(request, method)
        return request

    def generate_response(self, method, encoded_response):
        return self.response_cls.get_decoded_instance(encoded_response)

    def get_headers(self):
        return {}

    def generate_paypal_url(self, path):
        base = PAYPAL_SANDBOX_URL
        if not self.config.is_sandbox:
            base = PAYPAL_URL
        return base + path

    def log_api_request(self, encoded, decoded, group_id=None):
        if group_id is not None:
            message = '(GID %s) Request: %s => %s'
            util.api_logger.info(message, group_id, decoded, encoded)
        else:
            util.api_logger.info('Request: %s => %s', decoded, encoded)

    def log_api_response(self, encoded, decoded, group_id=None):
        params, messages = [], []
        if group_id is not None:
            messages.append('(GID %s)')
            params.append(group_id)

        correlation_id = decoded.get('correlationid', None)
        if correlation_id:
            messages.append('Response: [%s]: %s => %s')
            params.extend((correlation_id, encoded, decoded))
        else:
            messages.append('Response: %s => %s')
            params.extend((encoded, decoded))

        message = ' '.join(messages)
        util.api_logger.info(message, *params)

    def __call__(self,
                 method,
                 endpoint=None,
                 payload=None,
                 **params):
        """
        """
        endpoint = endpoint if endpoint else self.config.endpoint
        if payload is None:
            payload = {}

        payload.update(params)

        headers = self.get_headers()
        request = self.generate_request(method, payload)
        encoded_request = request.encode()
        group_id = self.generate_group_id()

        self.log_api_request(encoded_request, request, group_id=group_id)

        response, code = self.execute_request(
            endpoint, encoded_request, headers=headers,
            logger=util.api_logger.error,
        )

        if response is None:
            return None

        decoded_response = self.generate_response(method, response)
        self.log_api_response(response, decoded_response, group_id=group_id)
        return decoded_response

    def execute_request(self, url, body, headers={}, logger=None):
        try:
            request = urllib2.Request(url, body, headers)
            response = urllib2.urlopen(request, None, self.http_timeout)
            body = response.read()
            code = response.getcode()
            util.api_logger.debug('PayPal response [%s]: %s', code, body)
            return (body, code)
        except (urllib2.HTTPError, urllib2.URLError) as e:
            if logger is not None:
                logger('Connection error: %s' % e.strerror)
            return None


class Client(BaseClient):
    pass
