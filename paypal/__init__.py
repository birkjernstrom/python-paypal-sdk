# -*- coding: utf-8 -*-

__all__ = [
    # Modules
    'client', 'util',

    # Client aliases
    'ExpressCheckoutRequest',
    'ExpressCheckoutResponse',
    'Config',
    'Client',

    # Utility aliases
    'ensure_unicode',
]

from paypal import client, util

###############################################################################
# ALIASES
###############################################################################

#----------------------------------------
# Client Aliases
#----------------------------------------

#: Alias for ``client.ExpressCheckoutRequest``
ExpressCheckoutRequest = client.ExpressCheckoutRequest
#: Alias for ``client.ExpressCheckoutResponse``
ExpressCheckoutResponse = client.ExpressCheckoutResponse
#: Alias for ``client.Config``
Config = client.Config
#: Alias for ``client.Client``
Client = client.Client

#----------------------------------------
# Utility Aliases
#----------------------------------------

#: Alias for ``util.ensure_unicode``
ensure_unicode = util.ensure_unicode
