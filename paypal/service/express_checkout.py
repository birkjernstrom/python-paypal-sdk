# -*- coding: utf-8 -*-

from paypal.service import core

###############################################################################
# API REQUEST & RESPONSE OBJECTS
###############################################################################

Request = core.UnderscoreConventionRequest


class Response(core.UnderscoreConventionResponse):
    def is_success(self, allow_warnings=True):
        if self.is_success_without_warning():
            return True

        if allow_warnings:
            return self.is_success_with_warning()
        return False

    def is_success_without_warning(self):
        return self['ack'] == 'Success'

    def is_success_with_warning(self):
        return self['ack'] == 'SuccessWithWarning'


###############################################################################
# HELPERS
###############################################################################

def generate_checkout_url(client, token):
    path = '/webscr?cmd=_express-checkout&token=%s' % token
    return client.generate_paypal_url(path)
