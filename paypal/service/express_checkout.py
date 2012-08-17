# -*- coding: utf-8 -*-

from paypal.service import core

###############################################################################
# API REQUEST & RESPONSE OBJECTS
###############################################################################

Request = core.PrefixConventionRequest


class Response(core.PrefixConventionResponse):
    def is_success(self):
        return self['ack'] == 'Success'


###############################################################################
# HELPERS
###############################################################################

def generate_checkout_url(client, token):
    path = '/webscr?cmd=_express-checkout&token=%s' % token
    return client.generate_paypal_url(path)
