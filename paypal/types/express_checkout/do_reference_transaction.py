# -*- coding: utf-8 -*-

from paypal.types import core
from paypal.types.express_checkout import base
from paypal import countries, currencies


###############################################################################
# MIXINS
###############################################################################

#: Alias for ``base.FilterMixin``
FilterMixin = base.FilterMixin
#: Alias for ``base.AddressMixin``
AddressMixin = base.AddressMixin


class PaymentDetailsMixin(core.BaseType):
    """Payment Details associated with a DoReferenceTransaction.

    The included fields in this payment details is rather unique
    in comparison with payment details in other methods included
    in the Express Checkout suite.

    Which is the reason it does not subclass anyone of the
    existing payment detail implementations.
    """
    #: (Required) The total cost of the transaction to the buyer. If shipping
    #: cost and tax charges are known, include them in this value. If not,
    #: this value should be the current subtotal of the order. If the
    #: transaction includes one or more one-time purchases, this field must be
    #: equal to the sum of the purchases. Set this field to ``0`` if the
    #: transaction does not include a one-time purchase such as when you set
    #: up a billing agreement for a recurring payment that is not immediately
    #: charged. When the field is set to ``0``, purchase-specific fields are
    #: ignored.
    #:
    #:
    #: Character length and limitations:
    #:     Value is a positive number which cannot exceed $10,000 USD in any
    #:     currency. It includes no currency symbol. It must have 2 decimal
    #:     places, the decimal separator must be a period (.), and the
    #:     optional thousands separator must be a comma (,).
    amt = core.MoneyField()

    #: (Optional) A 3-character currency code (default is USD).
    currencycode = core.StringField(choices=currencies.codes)

    #: (Optional) Sum of cost of all items in this order.
    #:
    #:
    #: Character length and limitations:
    #:     Value is a positive number which cannot exceed $10,000 USD in any
    #:     currency. It includes no currency symbol. It must have 2 decimal
    #:     places, the decimal separator must be a period (.), and the
    #:     optional thousands separator must be a comma (,).
    #:
    #:
    #: Notes:
    #:     ``ITEMAMT`` is required if you specify ``L_AMTn``.
    itemamt = core.MoneyField()

    #: (Optional) Total shipping costs for this order.
    #:
    #:
    #: Character length and limitations:
    #:     Value is a positive number which cannot exceed $10,000 USD in any
    #:     currency. It includes no currency symbol. It must have 2 decimal
    #:     places, the decimal separator must be a period (.), and the
    #:     optional thousands separator must be a comma (,).
    #:
    #:
    #: Notes:
    #:     If you specify a value for ``SHIPPINGAMT``, you must also specify a
    #:     value for ``ITEMAMT``.
    shippingamt = core.MoneyField()

    #: (Optional) Total handling costs for this order.
    #:
    #:
    #: Character length and limitations:
    #:     Value is a positive number which cannot exceed $10,000 USD in any
    #:     currency. It includes no currency symbol. It must have 2 decimal
    #:     places, the decimal separator must be a period (.), and the
    #:     optional thousands separator must be a comma (,).
    #:
    #:
    #: Notes:
    #:     If you specify a value for ``HANDLINGAMT``, you must also specify a
    #:     value for ``ITEMAMT``.
    handlingamt = core.MoneyField()

    #: (Optional) Sum of tax for all items in this order.
    #:
    #:
    #: Character length and limitations:
    #:     Value is a positive number which cannot exceed $10,000 USD in any
    #:     currency. It includes no currency symbol. It must have 2 decimal
    #:     places, the decimal separator must be a period (.), and the
    #:     optional thousands separator must be a comma (,).
    #:
    #:
    #: Notes:
    #:     ``TAXAMT`` is required if you specify ``L_TAXAMTn``
    taxamt = core.MoneyField()

    #: (Optional) Description of items the buyer is purchasing.
    #:
    #:
    #: Character length and limitations:
    #:     127 single-byte alphanumeric characters
    #:
    #:
    #: Notes:
    #:     The value you specify is available only if the transaction includes
    #:     a purchase. This field is ignored if you set up a billing agreement
    #:     for a recurring payment that is not immediately charged.
    desc = core.StringField(max_length=127)

    #: (Optional) A free-form field for your own use.
    #:
    #:
    #: Character length and limitations:
    #:     256 single-byte alphanumeric characters
    #:
    #:
    #: Notes:
    #:     The value you specify is available only if the transaction includes
    #:     a purchase. This field is ignored if you set up a billing agreement
    #:     for a recurring payment that is not immediately charged.
    custom = core.StringField(max_length=256)

    #: (Optional) Your own invoice or tracking number.
    #:
    #:
    #: Character length and limitations:
    #:     256 single-byte alphanumeric characters
    #:
    #:
    #: Notes:
    #:     The value you specify is available only if the transaction includes
    #:     a purchase. This field is ignored if you set up a billing agreement
    #:     for a recurring payment that is not immediately charged.
    invnum = core.StringField(max_length=256)

    #: (Optional) An identification code for use by third-party applications
    #: to identify transactions.
    #:
    #:
    #: Character length and limitations:
    #:     32 single-byte alphanumeric characters
    buttonsource = core.StringField(max_length=32)

    #: (Optional) Your URL for receiving Instant Payment Notification (IPN)
    #: about this transaction. If you do not specify this value in the
    #: request, the notification URL from your Merchant Profile is used, if
    #: one exists.
    #:
    #:
    #: Character length and limitations:
    #:     2,048 single-byte alphanumeric characters
    #:
    #:
    #: Notes:
    #:     The notify URL applies only to ``DoExpressCheckoutPayment``. This
    #:     value is ignored when set in ``SetExpressCheckout`` or
    #:     ``GetExpressCheckoutDetails``.
    notifyurl = core.URLField(max_length=2048)

    #: ``ns:RecurringFlagType``
    #:
    #: (Optional) Flag to indicate a recurring transaction. It is one of the
    #: following values:
    #:
    #:
    #:     Any value other than ``Y`` – This is not a recurring transaction
    #:     (default).
    #:
    #:     ``Y`` – This is a recurring transaction.
    #:
    #:
    #: Notes:
    #:     To pass ``Y`` in this field, you must have established a billing
    #:     agreement with the buyer specifying the amount, frequency, and
    #:     duration of the recurring payment.
    recurring = core.StringField()


class ReferenceCreditCardMixin(core.BaseType):
    """The params related to a referenced credit card."""
    #: (Optional) Type of credit card. Is one of the following values:
    #:
    #:
    #:     ``Visa``
    #:
    #:     ``MasterCard``
    #:
    #:     ``Discover``
    #:
    #:     ``Amex``
    #:
    #:     ``Maestro``: See note.
    #:
    #:
    #: Character length and limitations:
    #:     Up to 10 single-byte alphabetic characters
    #:
    #:
    #: Notes:
    #:     If the credit card type is ``Maestro``, you must set
    #:     ``CURRENCYCODE`` to ``GBP``. In addition, you must specify either
    #:     ``STARTDATE`` or ``ISSUENUMBER``.
    #:
    #:
    #: For UK, only ``Maestro``, ``MasterCard``, ``Discover``, and ``Visa``
    #: are allowable. For Canada, only ``MasterCard`` and ``Visa`` are
    #: allowable. Interac debit cards are not supported.
    creditcardtype = core.StringField(choices=(
        'Visa', 'MasterCard', 'Discover', 'Amex', 'Maestro',
    ))

    #: (Optional) Credit card number.
    #:
    #:
    #: Character length and limitations:
    #:     Numeric characters only with no spaces or punctuation. The string
    #:     must conform with modulo and length required by each credit card
    #:     type.
    acct = core.StringField()

    #: Credit card expiration date. This field is required if you are using
    #: recurring payments with direct payments.
    #:
    #:
    #: Character length and limitations:
    #:     6 single-byte alphanumeric characters, including leading zero, in
    #:     the format MMYYYY
    expdate = core.StringField(max_length=6)

    #: (Optional) Card Verification Value, version 2. To comply with credit
    #: card processing regulations, you must not store this value after a
    #: transaction has been completed.
    #:
    #:
    #: Character length and limitations:
    #:     For Visa, MasterCard, and Discover, the value is exactly 3 digits.
    #:     For American Express, the value is exactly 4 digits.
    cvv2 = core.StringField(max_length=4)

    #: (Optional) Month and year that Maestro card was issued.
    #:
    #:
    #: Character length and limitations:
    #:     Must be 6 digits, including leading zero, in the format MMYYYY
    startdate = core.StringField(length=6)

    #: (Optional) Issue number of Maestro card.
    #:
    #:
    #: Character length and limitations:
    #:     2 numeric digits maximum.
    issuenumber = core.StringField(max_length=2)


class PayerInfoMixin(core.BaseType):
    """The params related to information about the payer."""
    #: (Optional) Email address of buyer.
    #:
    #:
    #: Character length and limitations:
    #:     127 single-byte characters
    email = core.StringField(max_length=127)

    #: (Required) Buyer's first name.
    #:
    #:
    #: Character length and limitations:
    #:     25 single-byte characters
    firstname = core.StringField(max_length=25)

    #: (Required) Buyer's last name.
    #:
    #:
    #: Character length and limitations:
    #:     25 single-byte characters
    lastname = core.StringField(max_length=25)


class PersonalAddressMixin(core.BaseType):
    """The home address of the buyer which is not necessarily
    the same as the shipping address.
    """
    #: (Optional) First street address.
    #:
    #:
    #: Character length and limitations:
    #:     100 single-byte characters
    street = core.StringField(max_length=100)

    #: (Optional) Second street address.
    #:
    #:
    #: Character length and limitations:
    #:     100 single-byte characters
    street2 = core.StringField(max_length=100)

    #: (Optional) Name of city.
    #:
    #:
    #: Character length and limitations:
    #:     40 single-byte characters
    city = core.StringField(max_length=40)

    #: (Optional) State or province.
    #:
    #:
    #: Character length and limitations:
    #:     40 single-byte characters
    state = core.StringField(max_length=40)

    #: (Optional) Country code.
    #:
    #: Character limit: 2 single-byte characters
    countrycode = core.StringField(choices=countries.codes)

    #: (Optional) U.S. ZIP code or other country-specific postal code.
    #:
    #:
    #: Character length and limitations:
    #:     20 single-byte characters
    zip = core.StringField(max_length=20)


###############################################################################
# TYPES
###############################################################################

#: Alias for ``base.BaseType``
BaseType = base.BaseType


class PaymentRequest(base.PaymentRequestWithReason):
    pass


class Request(BaseType,
              AddressMixin,
              PaymentDetailsMixin,
              base.PaymentItemDimensionDetailsMixin,
              ReferenceCreditCardMixin,
              PayerInfoMixin,
              PersonalAddressMixin):
    """DoReferenceTransaction Request Type."""
    method = core.ConstantField('DoReferenceTransaction')

    #: (Required) A transaction ID from a previous purchase, such as a credit
    #: card charge using the ``DoDirectPayment`` API, or a billing agreement
    #: ID.
    referenceid = core.StringField()

    #: (Optional) How you want to obtain payment. It is one of the following
    #: values:
    #:
    #:     ``Authorization`` – This payment is a basic authorization subject
    #:     to settlement with PayPal Authorization and Capture.
    #:
    #:     ``Sale`` – This is a final sale for which you are requesting
    #:     payment.
    paymentaction = core.StringField(choices=('Authorization', 'Sale'))

    #: (Optional) IP address of the buyer's browser.
    #:
    #:
    #: Character length and limitations:
    #:     15 single-byte characters, including periods, for example,
    #:     255.255.255.255
    #:
    #:
    #: Notes:
    #:     PayPal records this IP addresses as a means to detect possible
    #:     fraud.
    ipaddress = core.StringField()

    #: Whether you require that the buyer's shipping address on file with
    #: PayPal be a confirmed address. You must have permission from PayPal to
    #: not require a confirmed address. It is one of the following values:
    #:
    #:     ``0`` – You do not require that the buyer's shipping address be a
    #:     confirmed address.
    #:
    #:     ``1`` – You require that the buyer's shipping address be a
    #:     confirmed address.
    #:
    #:
    #: Character length and limitations:
    #:     1 single-byte numeric character
    #:
    #:
    #: Notes:
    #:     Setting this field overrides the setting you have specified in your
    #:     Merchant Account Profile.
    reqconfirmshipping = core.BooleanField()

    #: (Optional) Flag to indicate whether you want the results returned by
    #: Fraud Management Filters. By default, you do not receive this
    #: information. It is one of the following values:
    #:
    #:     ``0`` – Do not receive FMF details (default)
    #:
    #:     ``1`` – Receive FMF details
    returnfmfdetails = core.BooleanField()

    #: (Optional) Per transaction description of the payment that is passed to
    #: the consumer's credit card statement.
    #:
    #: If the API request provides a value for the soft descriptor field, the
    #: full descriptor displayed on the buyer's statement has the following
    #: format:
    #:
    #: ``<PP * | PAYPAL *><Merchant descriptor as set in the Payment Receiving
    #: Preferences><1 space><soft descriptor>``
    #:
    #: The soft descriptor can contain only the following characters:
    #:
    #:     Alphanumeric characters
    #:
    #:     - (dash)
    #:
    #:     * (asterisk)
    #:
    #:     . (period)
    #:
    #:     {space}
    #:
    #:     The PayPal prefix toggle is set to PAYPAL * in PayPal's
    #:     administration tools.
    #:
    #:     The merchant descriptor set in the Payment Receiving Preferences is
    #:     set to EBAY.
    #:
    #:     The soft descriptor is passed in as JanesFlowerGifts LLC
    #:
    #:
    #: If you use any other characters (such as ","), PayPal returns an error
    #: code. The soft descriptor does not include the phone number, which can
    #: be toggled between the merchant's customer service number and PayPal's
    #: customer service number. The maximum length of the total soft
    #: descriptor is 22 characters. Of this, the PayPal prefix uses either 4
    #: or 8 characters shown in the data format. Thus, the maximum length of
    #: the soft descriptor passed in the API request is:
    #:
    #: ``22 - len(<PP * | PAYPAL *>) - len(<Descriptor set in Payment
    #: Receiving Preferences> + 1)``
    #:
    #: For example, assume the following conditions:
    #:
    #: The resulting descriptor string on the credit card would be:
    #:
    #: ``PAYPAL *EBAY JanesFlow``
    softdescriptor = core.StringField()

    #: List of ``PaymentRequestType`` instances
    paymentrequest = core.ListTypeField(instanceof=PaymentRequest,
                                        required=True)


class Response(base.BaseType,
               FilterMixin):
    """DoReferenceTransaction Response Type."""
    #: Address Verification System response code.
    #:
    #: Character limit: 1 single-byte alphanumeric character
    avscode = core.StringField(length=1)

    #: Result of the CVV2 check by PayPal.
    cvv2match = core.StringField()

    #: Billing agreement identifier returned if the value of ``ReferenceID``
    #: in the request is a billing agreement identification number.
    billingagreementid = core.StringField()

    #: Response code from the processor when a recurring transaction is
    #: declined. For details on the meanings of the codes, see the
    #: Documentation_.
    #:
    #:
    #: Available since API version: 84.0
    #:
    #: .. _Documentation: https://merchant.paypal.com/us/cgi-bin/?&cmd=_render-content&content_ID=merchant/cc_compliance_error_codes
    paymentadvicecode = core.StringField()

    #: Unique transaction ID of the payment. You can specify up to 10
    #: payments, where n is a digit between 0 and 9, inclusive.
    #:
    #:
    #: Character length and limitations:
    #:     19 single-byte characters
    #:
    #:
    #: Notes:
    #:     If the ``PaymentAction`` of the request was ``Authorization`` or
    #:     ``Order``, this value is your ``AuthorizationID`` for use with the
    #:     Authorization & Capture APIs.
    transactionid = core.StringField(max_length=19)

    #: Parent or related transaction identification number. This field is
    #: populated for the following transaction types:
    #:
    #:     Reversal
    #:
    #:     Capture of an authorized transaction
    #:
    #:     Reauthorization of a transaction
    #:
    #:     Capture of an order. The value of ``ParentTransactionID`` is the
    #:     original ``OrderID``.
    #:
    #:     Authorization of an order. The value of ``ParentTransactionID`` is
    #:     the original ``OrderID``.
    #:
    #:     Capture of an order authorization
    #:
    #:     Void of an order. The value of ``ParentTransactionID`` is the
    #:     original ``OrderID``.
    #:
    #:
    #: Character length and limits: 19 single-byte characters maximum.
    parenttransactionid = core.StringField()

    #: Character length and limitations:
    #:     16 digits in xxxx-xxxx-xxxx-xxxx format.
    receiptid = core.StringField(max_length=19)

    #: Type of transaction. You can specify up to 10 payments, where n is a
    #: digit between 0 and 9, inclusive. It is one of the following values:
    #:
    #:
    #:     ``cart``
    #:
    #:     ``express-checkout``
    #:
    #:
    #: Character length and limitations:
    #:     15 single-byte characters
    transactiontype = core.StringField(choices=('cart', 'express-checkout'))

    #: Indicates whether the payment is instant or delayed. It is one of the
    #: following values:
    #:
    #: You can specify up to 10 payments, where n is a digit between 0 and 9,
    #: inclusive. It is one of the following values:
    #:
    #:
    #:     ``none``
    #:
    #:     ``echeck``
    #:
    #:     ``instant``
    #:
    #:
    #: Character length and limitations:
    #:     7 single-byte characters
    paymenttype = core.StringField(choices=('none', 'echeck', 'instant'))

    #: Time/date stamp of payment.
    #:
    #:
    #: Character length and limitations:
    #:     Date and time are in UTC/GMT format, for example,
    #:     ``2011-06-24T05:38:48Z``
    ordertime = core.UTCDatetimeField()

    #: The final amount charged, including any shipping and taxes from your
    #: Merchant Profile. You can specify up to 10 payments, where n is a digit
    #: between 0 and 9, inclusive.
    #:
    #:
    #: Character length and limitations:
    #:     Value is a positive number which cannot exceed $10,000 USD in any
    #:     currency. It includes no currency symbol. It must have 2 decimal
    #:     places, the decimal separator must be a period (.), and the
    #:     optional thousands separator must be a comma (,).
    amt = core.MoneyField()

    #: A 3-character currency code. Default: USD.
    currencycode = core.StringField(choices=currencies.codes)

    #: PayPal fee amount charged for the transaction. You can specify up to 10
    #: payments, where n is a digit between 0 and 9, inclusive.
    #:
    #:
    #: Character length and limitations:
    #:     Value is a positive number which cannot exceed $10,000 USD in any
    #:     currency. It includes no currency symbol. It must have 2 decimal
    #:     places, the decimal separator must be a period (.), and the
    #:     optional thousands separator must be a comma (,).
    feeamt = core.MoneyField()

    #: Amount deposited in your PayPal account after a currency conversion.
    #: You can specify up to 10 payments, where n is a digit between 0 and 9,
    #: inclusive.
    #:
    #:
    #: Character length and limitations:
    #:     Value is a positive number which cannot exceed $10,000 USD in any
    #:     currency. It includes no currency symbol. It must have 2 decimal
    #:     places, the decimal separator must be a period (.), and the
    #:     optional thousands separator must be a comma (,).
    settleamt = core.MoneyField()

    #: Tax charged on the transaction.
    #:
    #: You can specify up to 10 payments, where n is a digit between 0 and 9,
    #: inclusive.
    #:
    #:
    #: Character length and limitations:
    #:     Value is a positive number which cannot exceed $10,000 USD in any
    #:     currency. It includes no currency symbol. It must have 2 decimal
    #:     places, the decimal separator must be a period (.), and the
    #:     optional thousands separator must be a comma (,).
    taxamt = core.MoneyField()

    #: Exchange rate if a currency conversion occurred. Relevant only if your
    #: are billing in their non-primary currency. If the buyer chooses to pay
    #: with a currency other than the non-primary currency, the conversion
    #: occurs in the buyer's account. You can specify up to 10 payments, where
    #: n is a digit between 0 and 9, inclusive.
    #:
    #: ``EXCHANGERATE`` is deprecated since version 63.0. Use
    #: ``PAYMENTINFO_0_EXCHANGERATE`` instead.
    #:
    #:
    #: Character length and limitations:
    #:     Decimal value that does not exceed 17 characters, including decimal
    #:     point
    exchangerate = core.MoneyField()

    #: The status of the payment. You can specify up to 10 payments, where n
    #: is a digit between 0 and 9, inclusive. It is one of the following
    #: values:
    #:
    #:     ``None`` – No status.
    #:
    #:     ``Canceled-Reversal`` – A reversal has been canceled; for example,
    #:     when you win a dispute and the funds for the reversal have been
    #:     returned to you.
    #:
    #:     ``Completed`` – The payment has been completed, and the funds have
    #:     been added successfully to your account balance.
    #:
    #:     ``Denied`` – You denied the payment. This happens only if the
    #:     payment was previously pending because of possible reasons
    #:     described for the ``PendingReason`` element.
    #:
    #:     ``Expired`` – the authorization period for this payment has been
    #:     reached.
    #:
    #:     ``Failed`` – The payment has failed. This happens only if the
    #:     payment was made from your buyer's bank account.
    #:
    #:     ``In-Progress`` – The transaction has not terminated, e.g. an
    #:     authorization may be awaiting completion.
    #:
    #:     ``Partially-Refunded`` – The payment has been partially refunded.
    #:
    #:     ``Pending`` – The payment is pending. See the ``PendingReason``
    #:     field for more information.
    #:
    #:     ``Refunded`` – You refunded the payment.
    #:
    #:     ``Reversed`` – A payment was reversed due to a chargeback or other
    #:     type of reversal. The funds have been removed from your account
    #:     balance and returned to the buyer. The reason for the reversal is
    #:     specified in the ``ReasonCode`` element.
    #:
    #:     ``Processed`` – A payment has been accepted.
    #:
    #:     ``Voided`` – An authorization for this transaction
    #:     has been voided.
    #:
    #:     ``Completed-Funds-Held`` – The payment has been completed, and the
    #:     funds have been added successfully to your pending balance.  See
    #:     the ``PAYMENTINFO_n_HOLDDECISION`` field for more information.
    paymentstatus = core.StringField(choices=(
        'None', 'Canceled-Reversal', 'Completed',
        'Denied', 'Expired', 'Failed', 'In-Progress',
        'Partially-Refunded', 'Pending', 'Reversed',
        'Processed', 'Voided', 'Completed-Funds-Held',
    ))

    #: Reason the payment is pending. You can specify up to 10 payments, where
    #: n is a digit between 0 and 9, inclusive. It is one of the following
    #: values:
    #:
    #:     ``none`` – No pending reason.
    #:
    #:     ``address`` – The payment is pending because your buyer did not
    #:     include a confirmed shipping address and your Payment Receiving
    #:     Preferences is set such that you want to manually accept or deny
    #:     each of these payments. To change your preference, go to the
    #:     ``Preferences`` section of your ``Profile``.
    #:
    #:     ``authorization`` – The payment is pending because it has been
    #:     authorized but not settled. You must capture the funds first.
    #:
    #:     ``echeck`` – The payment is pending because it was made by an
    #:     eCheck that has not yet cleared.
    #:
    #:     ``intl`` – The payment is pending because you hold a non-U.S.
    #:     account and do not have a withdrawal mechanism. You must manually
    #:     accept or deny this payment from your ``Account Overview``.
    #:
    #:     ``multi-currency`` – You do not have a balance in the currency
    #:     sent, and you do not have your ``Payment Receiving Preferences``
    #:     set to automatically convert and accept this payment. You must
    #:     manually accept or deny this payment.
    #:
    #:     ``order`` – The payment is pending because it is part of an order
    #:     that has been authorized but not settled.
    #:
    #:     ``paymentreview`` – The payment is pending while it is being
    #:     reviewed by PayPal for risk.
    #:
    #:     ``unilateral`` – The payment is pending because it was made to an
    #:     email address that is not yet registered or confirmed.
    #:
    #:     ``verify`` – The payment is pending because you are not yet
    #:     verified. You must verify your account before you can accept this
    #:     payment.
    #:
    #:     ``other`` – The payment is pending for a reason other than those
    #:     listed above. For more information, contact PayPal customer
    #:     service.
    #:
    #:
    #: Notes:
    #:     ``PendingReason`` is returned in the response only if
    #:     ``PaymentStatus`` is ``Pending``.
    pendingreason = core.StringField(choices=(
        'none', 'address', 'authorization', 'echeck',
        'intl', 'multi-currency', 'order', 'paymentreview',
        'unilateral', 'verify', 'other',
    ))

    #: Reason for a reversal if TransactionType is reversal. You can specify
    #: up to 10 payments, where n is a digit between 0 and 9, inclusive. It is
    #: one of the following values:
    #:
    #:     ``none`` – No reason code.
    #:
    #:     ``chargeback`` – A reversal has occurred on this
    #:     transaction due to a chargeback by your buyer.
    #:
    #:     ``guarantee`` – A reversal has occurred on this transaction due to
    #:     your buyer triggering a money-back guarantee.
    #:
    #:     ``buyer-complaint`` – A reversal has occurred on this transaction
    #:     due to a complaint about the transaction from your buyer.
    #:
    #:     ``refund`` – A reversal has occurred on this transaction because
    #:     you have given the buyer a refund.
    #:
    #:     ``other`` – A reversal has occurred on this transaction due to a
    #:     reason not listed above.
    reasoncode = core.StringField(choices=(
        'none', 'chargeback', 'guarantee',
        'buyer-complaint', 'refund', 'other',
    ))

    #: Prior to version 64.4, the kind of seller protection in force for the
    #: transaction. You can specify up to 10 payments, where n is a digit
    #: between 0 and 9, inclusive. It is one of the following values:
    #:
    #:     ``None``
    #:
    #:     ``Eligible`` – Merchant is protected by PayPal's Seller Protection
    #:     Policy for Unauthorized Payments and Item Not Received.
    #:
    #:     ``PartiallyEligible`` – Merchant is protected by PayPal's Seller
    #:     Protection Policy for Item Not Received.
    #:
    #:     ``PartiallyEligible`` - INR only.
    #:
    #:     ``PartiallyEligible`` - Unauth only.
    #:
    #:     ``Ineligible`` – Merchant is not protected under the Seller
    #:     Protection Policy.
    protectioneligibility = core.StringField(choices=(
        'None', 'Eligible', 'PartiallyEligible', 'Ineligible',
    ))

    #: Since version 64.4, the kind of seller protection in force for the
    #: transaction. You can specify up to 10 payments, where n is a digit
    #: between 0 and 9, inclusive. It is one of the following values:
    #:
    #:     ``None``
    #:
    #:     ``ItemNotReceivedEligible`` – Merchant is protected by PayPal's
    #:     Seller Protection Policy for Item Not Received
    #:
    #:     ``UnauthorizedPaymentEligible`` – Merchant is protected
    #:     by PayPal's Seller Protection Policy for Unauthorized Payment li>
    #:
    #:     ``ItemNotReceivedEligible``, ``UnauthorizedPaymentEligible``
    #:
    #:
    #: Available since API version: 64.4
    protectioneligibilitytype = core.StringField(choices=(
        'None', 'ItemNotReceivedEligible',
        'UnauthorizedPaymentEligible', 'ItemNotReceivedEligible',
    ))

    #: Store ID as entered in the transaction
    storeid = core.StringField()

    #: Terminal ID as entered in the transaction
    terminalid = core.StringField()
