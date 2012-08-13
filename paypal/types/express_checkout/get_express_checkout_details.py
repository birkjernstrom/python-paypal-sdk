# -*- coding: utf-8 -*-

from paypal.types import core
from paypal.types.express_checkout import base
from paypal import countries


###############################################################################
# MIXINS
###############################################################################

#: Alias for ``base.AddressMixin``
AddressMixin = base.AddressMixin
#: Alias for ``base.PaymentDetailsMixin``
PaymentDetailsMixin = base.PaymentDetailsMixin
#: Alias for ``base.PaymentItemDetailsMixin``
PaymentItemDetailsMixin = base.PaymentItemDetailsMixin
#: Alias for ``base.eBayPaymentDetailsMixin``
eBayPaymentDetailsMixin = base.eBayPaymentDetailsMixin
#: Alias for ``base.SellerDetailsMixin``
SellerDetailsMixin = base.SellerDetailsMixin
#: Alias for ``base.TaxDetailsMixin``
TaxDetailsMixin = base.TaxDetailsMixin


class PayerInformationMixin(core.BaseType):
    """The params related to the payer information within a ``Response``."""
    #: Email address of buyer.
    #:
    #:
    #: Character length and limitations:
    #:     127 single-byte characters
    email = core.StringField(max_length=127)

    #: Unique PayPal Customer Account identification number.
    #:
    #:
    #: Character length and limitations:
    #:     13 single-byte alphanumeric characters
    payerid = core.StringField(max_length=13)

    #: Status of buyer. It is one of the following values:
    #:
    #:
    #:     ``verified``
    #:
    #:     ``unverified``
    #:
    #:
    #: Character length and limitations:
    #:     10 single-byte alphabetic characters
    payerstatus = core.StringField(choices=('verified', 'unverified'))

    #: Buyer’s country of residence in the form of ISO standard 3166
    #: two-character country codes.
    #:
    #:
    #: Character length and limitations:
    #:     2 single-byte characters
    countrycode = core.StringField(choices=countries.codes)

    #: Buyer’s business name.
    #:
    #:
    #: Character length and limitations:
    #:     127 single-byte characters
    business = core.StringField(max_length=127)


class PayerNameMixin(core.BaseType):
    """The params related to the payers name within a ``Response``."""
    #: Buyer’s salutation.
    #:
    #:
    #: Character length and limitations:
    #:     20 single-byte characters
    salutation = core.StringField(max_length=20)

    #: Buyer’s first name.
    #:
    #:
    #: Character length and limitations:
    #:     25 single-byte characters
    firstname = core.StringField(max_length=25)

    #: Buyer’s middle name.
    #:
    #:
    #: Character length and limitations:
    #:     25 single-byte characters
    middlename = core.StringField(max_length=25)

    #: Buyer’s last name.
    #:
    #:
    #: Character length and limitations:
    #:     25 single-byte characters
    lastname = core.StringField(max_length=25)

    #: Buyer’s suffix.
    #:
    #:
    #: Character length and limitations:
    #:     12 single-byte characters
    suffix = core.StringField(max_length=12)


class AddressMixin(base.AddressMixin):
    """Extended version of ExpressCheckout AddressType
    which contains the address status as well.

    This mixin is intended to be utilized with the response type
    in GetExpressCheckoutDetails.
    """
    #: Status of street address on file with PayPal. You can specify up to 10
    #: payments, where n is a digit between 0 and 9, inclusive. It is one of
    #: the following values:
    #:
    #:     ``none``
    #:
    #:     ``Confirmed``
    #:
    #:     ``Unconfirmed``
    addressstatus = core.StringField(choices=(
        'none', 'Confirmed', 'Unconfirmed',
    ))


class UserSelectedOptionsMixin(core.BaseType):
    """The params related to the user selected
    options within a ``PaymentRequest``.

    """
    #: Describes how the options that were presented to the buyer were
    #: determined. It is one of the following values:
    #:
    #:     ``API - Callback``
    #:
    #:     ``API - Flatrate``
    shippingcalculationmode = core.StringField(choices=(
        'API - Callback', 'API - Flatrate',  # Really PayPal, really?
    ))

    #: The option that the buyer chose for insurance. It is one of the
    #: following values:
    #:
    #:     ``Yes`` – The buyer opted for insurance.
    #:
    #:     ``No`` – The buyer did not opt for insurance.
    insuranceoptionselected = core.StringField(choices=('Yes', 'No'))

    #: Indicates whether the buyer chose the default shipping option. It is
    #: one of the following values:
    #:
    #:     ``true`` – The buyer chose the default shipping option.
    #:
    #:     ``false`` – The buyer did not choose the default shipping option.
    #:
    #:
    #: Character length and limitations:
    #:     true or false
    shippingoptionisdefault = core.StringField(choices=('true', 'false'))

    #: The shipping amount that the buyer chose.
    #:
    #:
    #: Character length and limitations:
    #:     Value is a positive number which cannot exceed $10,000 USD in any
    #:     currency. It includes no currency symbol. It must have 2 decimal
    #:     places, the decimal separator must be a period (.), and the
    #:     optional thousands separator must be a comma (,).
    shippingoptionamount = core.MoneyField()

    #: The name of the shipping option, such as air or ground.
    shippingoptionname = core.StringField()


class PaymentRequestInfoMixin(core.BaseType):
    #: Transaction ID for up to 10 parallel payment requests. You can specify
    #: up to 10 payments, where n is a digit between 0 and 9, inclusive.
    #:
    #:
    #: Available since API version: 64.0
    transactionid = core.StringField()

    #: Payment request ID. You can specify up to 10 payments, where n is a
    #: digit between 0 and 9, inclusive.
    #:
    #:
    #: Available since API version: 64.0
    paymentrequestid = core.StringField()


###############################################################################
# TYPES
###############################################################################

#: Alias for ``base.BaseType``
BaseType = base.BaseType


class PaymentRequest(base.PaymentRequest,
                     PaymentRequestInfoMixin):
    """Payment Request Package."""


class PaymentInfo(BaseType, SellerDetailsMixin):
    #: Payment error short message. You can specify up to 10 payments, where n
    #: is a digit between 0 and 9, inclusive.
    shortmessage = core.StringField()

    #: Payment error long message. You can specify up to 10 payments, where n
    #: is a digit between 0 and 9, inclusive.
    longmessage = core.StringField()

    #: Payment error code. You can specify up to 10 payments, where n is a
    #: digit between 0 and 9, inclusive.
    errorcode = core.StringField()

    #: Payment error severity code. You can specify up to 10 payments, where n
    #: is a digit between 0 and 9, inclusive.
    severitycode = core.StringField()

    #: Application-specific error values indicating more about the error
    #: condition. You can specify up to 10 payments, where n is a digit
    #: between 0 and 9, inclusive.
    ack = core.StringField()


class Request(BaseType):
    """GetExpressCheckoutDetails Request Type."""
    #: (Required) Must be GetExpressCheckoutDetails.
    method = core.ConstantField('GetExpressCheckoutDetails')

    #: (Required) A timestamped token, the value of which was returned by
    #: ``SetExpressCheckout`` response.
    #:
    #:
    #: Character length and limitations:
    #:     20 single-byte characters
    token = core.StringField(max_length=20)


class Response(BaseType,
               PayerInformationMixin,
               AddressMixin,
               UserSelectedOptionsMixin,
               TaxDetailsMixin):
    """GetExpressCheckoutDetails Response Type."""
    #: The timestamped token value that was returned by ``SetExpressCheckout``
    #: response and passed on ``GetExpressCheckoutDetails`` request.
    #:
    #:
    #: Character length and limitations:
    #:     20 single-byte characters
    token = core.StringField(max_length=20)

    #: A free-form field for your own use, as set by you in the ``Custom``
    #: element of the ``SetExpressCheckout`` request.
    #:
    #:
    #: Character length and limitations:
    #:     256 single-byte alphanumeric characters
    custom = core.StringField(max_length=256)

    #: Your own invoice or tracking number, as set by you in the element of
    #: the same name in the ``SetExpressCheckout`` request.
    #:
    #:
    #: Character length and limitations:
    #:     127 single-byte alphanumeric characters
    invnum = core.StringField(max_length=127)

    #: Buyer’s contact phone number.
    #:
    #:
    #: Character length and limitations:
    #:     Field mask is XXX-XXX-XXXX (for US numbers) or +XXX XXXXXXXX (for
    #:     international numbers)
    #:
    #:
    #: Notes:
    #:     PayPal returns a contact phone number only if your Merchant Account
    #:     Profile settings require that the buyer enter one.
    phonenum = core.StringField()

    #: A discount or gift certificate offered by PayPal to the buyer. This
    #: amount is represented by a negative amount. If the buyer has a negative
    #: PayPal account balance, PayPal adds the negative balance to the
    #: transaction amount, which is represented as a positive value.
    #:
    #:
    #: Character length and limitations:
    #:     Must not exceed $10,000 USD in any currency. No currency symbol.
    #:     Must have 2 decimal places, decimal separator must be a period (.),
    #:     and the optional thousands separator must be a comma (,).
    paypaladjustment = core.MoneyField()

    #: Flag to indicate whether you need to redirect the buyer back to PayPal
    #: after successfully completing the transaction.
    #:
    #:
    #: Notes:
    #:     Use this field only if you are using giropay or bank transfer
    #:     payment methods in Germany.
    redirectrequired = core.BooleanField()

    #: Status of the checkout session. If payment is completed, the
    #: transaction identification number of the resulting transaction is
    #: returned. It is one of the following values:
    #:
    #:     ``PaymentActionNotInitiated``
    #:
    #:     ``PaymentActionFailed``
    #:
    #:     ``PaymentActionInProgress``
    #:
    #:     ``PaymentCompleted``
    checkoutstatus = core.StringField(choices=(
        'PaymentActionNotInitiated',
        'PaymentActionFailed',
        'PaymentActionInProgress'
        'PaymentCompleted',
    ))

    #: Gift message entered by the buyer on the PayPal checkout pages.
    #:
    #:
    #: Character length and limitations:
    #:     150 single-byte characters
    giftmessage = core.StringField(max_length=150)

    #: Whether the buyer requested a gift receipt. It is one of the following
    #: values:
    #:
    #:     ``true`` – The buyer requested a gift receipt.
    #:
    #:     ``false`` – The buyer did not request a gift receipt.
    giftreceiptenable = core.StringField(choices=('true', 'false'))

    #: Returns the gift wrap name only if the buyer selects gift option on the
    #: PayPal pages.
    #:
    #:
    #: Character length and limitations:
    #:     25 single-byte characters
    giftwrapname = core.StringField(max_length=25)

    #: Returns the gift wrap amount only if the buyer selects the gift option
    #: on the PayPal pages.
    #:
    #:
    #: Character length and limitations:
    #:     Must not exceed $10,000 USD in any currency. No currency symbol.
    #:     Must have two decimal places, decimal separator must be a period
    #:     (.), and the optional thousands separator must be a comma (,).
    giftwrapamount = core.MoneyField()

    #: Buyer’s email address if the buyer provided it on the PayPal pages.
    #:
    #:
    #: Character length and limitations:
    #:     127 single-byte characters
    buyermarketingemail = core.StringField(max_length=127)

    #: Survey question on the PayPal checkout pages.
    #:
    #:
    #: Character length and limitations:
    #:     50 single-byte characters
    surveyquestion = core.StringField(max_length=50)

    #: Survey response the buyer selects on the PayPal pages.
    #:
    #:
    #: Character length and limitations:
    #:     15 single-byte characters
    surveychoiceselected = core.StringField(max_length=15)

    #: List of ``PaymentRequestType`` instances
    paymentrequest = core.ListTypeField(instanceof=PaymentRequest,
                                        required=True)

    #: List of ``PaymentInfo`` instances
    paymentinfo = core.ListTypeField(instanceof=PaymentInfo,
                                     required=True)
