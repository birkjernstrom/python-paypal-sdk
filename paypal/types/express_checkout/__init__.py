# -*- coding: utf-8 -*-

__all__ = [
    'set_express_checkout',
    'get_express_checkout_details',
    'do_express_checkout',
    'do_reference_transaction',
]

from paypal.types.express_checkout import (
    set_express_checkout,
    get_express_checkout_details,
    do_express_checkout,
    do_reference_transaction,
)

###############################################################################
# ALIASES
###############################################################################

#----------------------------------------
# SetExpressCheckout Aliases
#----------------------------------------

#: Alias for ``set_express_checkout.Request``
SetExpressCheckoutRequest = set_express_checkout.Request
#: Alias for ``set_express_checkout.Response``
SetExpressCheckoutResponse = set_express_checkout.Response

#----------------------------------------
# GetExpressCheckoutDetails Aliases
#----------------------------------------

#: Alias for ``get_express_checkout_details.Request``
GetExpressCheckoutDetailsRequest = get_express_checkout_details.Request
#: Alias for ``get_express_checkout_details.Response``
GetExpressCheckoutDetailsResponse = get_express_checkout_details.Response

#----------------------------------------
# DoExpressCheckout Aliases
#----------------------------------------

#: Alias for ``do_express_checkout.Request``
DoExpressCheckoutRequest = do_express_checkout.Request
#: Alias for ``do_express_checkout.Response``
DoExpressCheckoutResponse = do_express_checkout.Response

#----------------------------------------
# DoReferenceTransaction Aliases
#----------------------------------------

#: Alias for ``do_reference_transaction.Request``
DoReferenceTransactionRequest = do_reference_transaction.Request
#: Alias for ``do_reference_transaction.Response``
DoReferenceTransactionResponse = do_reference_transaction.Response
