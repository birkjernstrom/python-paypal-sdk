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
    'logger',
    'api_logger',
    'ipn_logger',
    'ensure_unicode',
    'generate_utc_string',
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

#: Alias for ``util.logger``
logger = util.logger
#: Alias for ``util.api_logger``
api_logger = util.api_logger
#: Alias for ``util.ipn_logger``
ipn_logger = util.ipn_logger
#: Alias for ``util.ensure_unicode``
ensure_unicode = util.ensure_unicode
#: Alias for ``util.generate_utc_string``
generate_utc_string = util.generate_utc_string

#----------------------------------------
# Instant Payment Notification Aliases
#----------------------------------------

#: Alias for ``ipn.Listener``
IPNListener = ipn.Listener
#: Alias for ``ipn.Notification``
IPNotification = ipn.Notification
