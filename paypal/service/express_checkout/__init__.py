# -*- coding: utf-8 -*-

__all__ = [
    # Modules
    'set_express_checkout',
    'get_express_checkout_details',
    'do_express_checkout_payment',
    'do_reference_transaction',

    # Aliases
    'SetExpressCheckoutRequest',
    'SetExpressCheckoutResponse',
    'GetExpressCheckoutDetailsRequest',
    'GetExpressCheckoutDetailsResponse',
    'DoExpressCheckoutPaymentRequest',
    'DoExpressCheckoutPaymentResponse',
    'DoReferenceTransactionRequest',
    'DoReferenceTransactionResponse',
]

from paypal.service.express_checkout import (
    set_express_checkout,
    get_express_checkout_details,
    do_express_checkout_payment,
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
# DoExpressCheckoutPayment Aliases
#----------------------------------------

#: Alias for ``do_express_checkout.Request``
DoExpressCheckoutPaymentRequest = do_express_checkout_payment.Request
#: Alias for ``do_express_checkout.Response``
DoExpressCheckoutPaymentResponse = do_express_checkout_payment.Response

#----------------------------------------
# DoReferenceTransaction Aliases
#----------------------------------------

#: Alias for ``do_reference_transaction.Request``
DoReferenceTransactionRequest = do_reference_transaction.Request
#: Alias for ``do_reference_transaction.Response``
DoReferenceTransactionResponse = do_reference_transaction.Response
