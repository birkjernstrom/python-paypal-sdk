# -*- coding: utf-8 -*-

__all__ = [
    # Modules
    'core',
    'express_checkout',

    # Core Aliases
    'Request',
    'Response',
    'UnderscoreConventionRequest',
    'UnderscoreConventionResponse',
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
#: Alias for ``core.UnderscoreConventionRequest``
UnderscoreConventionRequest = core.UnderscoreConventionRequest
#: Alias for ``core.UnderscoreConventionResponse``
UnderscoreConventionResponse = core.UnderscoreConventionResponse

#----------------------------------------
# Express Checkout Aliases
#----------------------------------------

#: Alias for ``express_checkout.Request``
ExpressCheckoutRequest = express_checkout.Request
#: Alias for ``express_checkout.Response``
ExpressCheckoutResponse = express_checkout.Response
