# -*- coding: utf-8 -*-

__all__ = [
    # Modules
    'core',
    'express_checkout',

    # Core Aliases
    'Request',
    'Response',
    'PrefixConventionRequest',
    'PrefixConventionResponse',
]

from paypal.service import core, express_checkout

###############################################################################
# ALIASES
###############################################################################

#----------------------------------------
# Core Aliases
#----------------------------------------

#: Alias for ``core.Request``
Request = core.Request
#: Alias for ``core.Response``
Response = core.Response
#: Alias for ``core.PrefixConventionRequest``
PrefixConventionRequest = core.PrefixConventionRequest
#: Alias for ``core.PrefixConventionResponse``
PrefixConventionResponse = core.PrefixConventionResponse

#----------------------------------------
# Express Checkout Aliases
#----------------------------------------

#: Alias for ``express_checkout.Request``
ExpressCheckoutRequest = express_checkout.Request
#: Alias for ``express_checkout.Response``
ExpressCheckoutResponse = express_checkout.Response
