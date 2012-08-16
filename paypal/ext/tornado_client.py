# -*- coding: utf-8 -*-

from tornado import gen
from tornado.httpclient import AsyncHTTPClient

from paypal import client


class AsyncClient(client.Client):
    @gen.engine
    def __call__(self,
                 method,
                 endpoint=None,
                 payload=None,
                 callback=None,
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

        httpclient = AsyncHTTPClient()
        response = yield gen.Task(httpclient.fetch, endpoint,
                                  method='POST', body=encoded_request,
                                  headers=headers)

        encoded = response.body
        r = self.generate_response(method, encoded)
        self.log_api_response(encoded, r, group_id=group_id)
        if callback:
            callback(r)
