# -*- coding: utf-8 -*-

__all__ = [
    # Modules
    'client', 'util', 'service', 'ipn',

    # Client aliases
    'ExpressCheckoutRequest',
    'ExpressCheckoutResponse',
    'Config',
    'Client',

    # Utility aliases
    'ensure_unicode',
]

from paypal import client, util, service, ipn

###############################################################################
# ALIASES
###############################################################################

#----------------------------------------
# Client Aliases
#----------------------------------------

#: Alias for ``client.Config``
Config = client.Config
#: Alias for ``client.Client``
Client = client.Client

#----------------------------------------
# Utility Aliases
#----------------------------------------

#: Alias for ``util.ensure_unicode``
ensure_unicode = util.ensure_unicode

#----------------------------------------
# Instant Payment Notification Aliases
#----------------------------------------

#: Alias for ``ipn.Listener``
IPNListener = ipn.Listener
#: Alias for ``ipn.Notification``
IPNotification = ipn.Notification
