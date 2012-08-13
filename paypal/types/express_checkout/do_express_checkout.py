# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

from paypal.types import core
from paypal.types.express_checkout import base
from paypal import currencies


###############################################################################
# MIXINS
###############################################################################

#: Alias for ``base.FilterMixin``
FilterMixin = base.FilterMixin
#: Alias for ``base.AddressMixin``
AddressMixin = base.AddressMixin
#: Alias for ``base.PaymentItemURLDetailsMixin``
PaymentItemURLDetailsMixin = base.PaymentItemURLDetailsMixin
#: Alias for ``base.PaymentItemDimensionDetailsMixin``
PaymentItemDimensionDetailsMixin = base.PaymentItemDimensionDetailsMixin
#: Alias for ``base.eBayPaymentDetailsMixin``
eBayPaymentDetailsMixin = base.eBayPaymentDetailsMixin
#: Alias for ``base.TaxDetailsMixin``
TaxDetailsMixin = base.TaxDetailsMixin
#: Alias for ``base.eBayPaymentCartDetailsMixin``
eBayPaymentCartDetailsMixin = base.eBayPaymentCartDetailsMixin


class PaymentDetailsMixin(base.PaymentDetailsWithActionMixin):
    #: A per transaction description of the payment that is passed to the
    #: buyer's credit card statement. You can specify up to 10 payments, where
    #: n is a digit between 0 and 9, inclusive.
    #:
    #:
    #: Notes:
    #:     Ignore when ``PAYMENTREQUEST_n_PAYMENTACTION=Order``.
    softdescriptor = core.StringField()


class SellerDetailsMixin(core.BaseType):
    """The params related to the seller details."""
    #: (Optional) Unique non-changing identifier for the merchant at the
    #: marketplace site. This ID is not displayed. You can specify up to 10
    #: payments, where n is a digit between 0 and 9, inclusive.
    #:
    #:
    #: Character length and limitations:
    #:     13 single-byte alphanumeric characters
    sellerid = core.StringField(max_length=13)

    #: (Optional) Current name of the merchant or business at the marketplace
    #: site. This name may be shown to the buyer. You can specify up to 10
    #: payments, where n is a digit between 0 and 9, inclusive.
    sellerusername = core.StringField()

    #: (Optional) Date when the merchant registered with the marketplace. You
    #: can specify up to 10 payments, where n is a digit between 0 and 9,
    #: inclusive.
    #:
    #:
    #: Character length and limitations:
    #:     Date and time are in UTC/GMT format, for example,
    #:     ``2011-06-24T05:38:48Z``
    sellerregistrationdate = core.UTCDatetimeField()


###############################################################################
# TYPES
###############################################################################

#: Alias for ``base.BaseType``
BaseType = base.BaseType


class PaymentRequest(base.PaymentRequest,
                     PaymentDetailsMixin,
                     PaymentItemDimensionDetailsMixin,
                     PaymentItemURLDetailsMixin,
                     SellerDetailsMixin,
                     eBayPaymentCartDetailsMixin):
    """Payment Request Package."""


class Request(BaseType, base.UserSelectedOptionsMixin):
    """DoExpressCheckout Request Type."""
    #: (Required) Must be DoExpressCheckoutPayment.
    method = core.ConstantField('DoExpressCheckout')

    #: (Required) The timestamped token value that was returned in the
    #: ``SetExpressCheckout`` response and passed in the
    #: ``GetExpressCheckoutDetails`` request.
    #:
    #:
    #: Character length and limitations:
    #:     20 single-byte characters
    token = core.StringField(max_length=20)

    #: (Required) Unique PayPal buyer account identification number as
    #: returned in the ``GetExpressCheckoutDetails`` response
    #:
    #:
    #: Character length and limitations:
    #:     13 single-byte alphanumeric characters
    payerid = core.StringField(max_length=13)

    #: (Optional) Flag to indicate whether you want the results returned by
    #: Fraud Management Filters. By default, you do not receive this
    #: information. It is one of the following values:
    #:
    #:     ``0`` – Do not receive FMF details (default).
    #:
    #:     ``1`` – Receive FMF details.
    returnfmfdetails = core.BooleanField()

    #: (Optional) The gift message the buyer entered on the PayPal pages.
    #:
    #:
    #: Character length and limitations:
    #:     150 single-byte characters
    giftmessage = core.StringField(max_length=150)

    #: (Optional) Whether the buyer selected a gift receipt on the PayPal
    #: pages. It is one of the following values:
    #:
    #:     ``true`` – The buyer selected a gift message.
    #:
    #:     ``false`` – The buyer did not select a gift message.
    giftreceiptenable = core.StringField(choices=('true', 'false'))

    #: (Optional) Return the gift wrap name only if the buyer selected the
    #: gift option on the PayPal pages.
    #:
    #:
    #: Character length and limitations:
    #:     25 single-byte characters
    giftwrapname = core.StringField(max_length=25)

    #: (Optional) Amount only if the buyer selected the gift option on the
    #: PayPal pages.
    #:
    #:
    #: Character length and limitations:
    #:     Value is a positive number which cannot exceed $10,000 USD in any
    #:     currency. It includes no currency symbol. It must have 2 decimal
    #:     places, the decimal separator must be a period (.), and the
    #:     optional thousands separator must be a comma (,).
    giftwrapamount = core.MoneyField()

    #: (Optional) The buyer email address opted in by the buyer on the PayPal
    #: pages.
    #:
    #:
    #: Character length and limitations:
    #:     127 single-byte characters
    buyermarketingemail = core.StringField(max_length=127)

    #: (Optional) Survey question on the PayPal pages.
    #:
    #: Limitations: 50 single-byte characters
    surveyquestion = core.StringField(max_length=50)

    #: (Optional) Survey response that the buyer selected on the PayPal pages.
    #:
    #:
    #:
    #: Character length and limitations:
    #:     15 single-byte characters
    surveychoiceselected = core.StringField(max_length=15)

    #: (Optional) Identification code for use by third-party applications to
    #: identify transactions.
    #:
    #:
    #: Character length and limitations:
    #:     32 single-byte alphanumeric characters
    buttonsource = core.StringField(max_length=32)

    #: List of ``PaymentRequestType`` instances
    paymentrequest = core.ListTypeField(instanceof=PaymentRequest,
                                        required=True)


class PaymentInfo(base.PaymentInfo,
                  base.SellerDetailsWithMerchantAccountMixin,
                  FilterMixin):
    #: Amount of shipping charged on this transaction.
    #:
    #: If you specify a value for ``PAYMENTINFO_n_SHIPPINGAMT``, you must also
    #: specify a value for ``PAYMENTINFO_n_ITEMAMT``.
    #:
    #:
    #: Character length and limitations:
    #:     Must not exceed $10,000 USD in any currency. No currency symbol.
    #:     Regardless of currency, decimal separator must be a period (.), and
    #:     the optional thousands separator must be a comma (,). Equivalent to
    #:     nine characters maximum for USD.
    shippingamt = core.MoneyField()

    #: Unique, non-changing identifier for the merchant at the marketplace
    #: site. (Optional)
    #:
    #: You can specify up to 10 payments, where '``n``' is a digit between 0
    #: and 9, inclusive.
    #:
    #:
    #: Character length and limitations:
    #:     13 single-byte alphanumeric characters.
    sellerid = core.StringField(max_length=13)

    #: Current name of the merchant or business at the marketplace site. This
    #: name may be shown to the buyer.
    #:
    #: You can specify up to 10 payments, where '``n``' is a digit between 0
    #: and 9, inclusive.
    sellerusername = core.StringField()

    #: Date when the merchant registered with the marketplace.
    #:
    #: You can specify up to 10 payments, where '``n``' is a digit between 0
    #: and 9, inclusive.
    #:
    #:
    #: Character length and limitations:
    #:     Date and time are in UTC/GMT format. For example:
    #:     ``2011-06-24T05:38:48Z``.
    sellerregistrationdate = core.UTCDatetimeField()

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

    #: eCheck latest expected clear date.
    expectedecheckcleardate = core.StringField()

    #: Shipping method selected by the user during check-out.
    shippingmethod = core.StringField()

    #: This field holds the category of the instrument only when it is
    #: promotional. Return value 1 represents BML.
    instrumentcategory = core.StringField()

    #: Code used to identify the promotion offer.
    offercode = core.StringField()

    #: Unique identification for merchant/buyer/offer combo.
    offertrackingid = core.StringField()

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

    #: Reason that this payment is being held. You can specify up to 10
    #: payments, where n is a digit between 0 and 9, inclusive. It is one of
    #: the following values:
    #:
    #:     ``newsellerpaymenthold`` – This is a new merchant.
    #:
    #:     ``paymenthold`` – A hold is placed on the merchant's transaction
    #:     for a reason not listed.
    #:
    #:     ``ExternalPaymentHold``
    #:
    #:     ``ReceiverExempt``
    #:
    #:     ``PaymentIneligible``
    #:
    #:     ``InvalidRequest``
    #:
    #:     ``SystemError``
    #:
    #:
    #: Available since API version: 71.0
    #: and is returned only if ``PAYMENTINFO_n_PAYMENTSTATUS ``
    #: is ``Completed-Funds-Held``
    holddecision = core.StringField(choices=(
        'newsellerpaymenthold', 'paymenthold',
        'ExternalPaymentHold', 'ReceiverExempt',
        'PaymentIneligible', 'InvalidRequest',
        'SystemError',
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

    #: eBay transaction identification number. You can specify up to 10
    #: payments, where n is a digit between 0 and 9, inclusive.
    #:
    #:
    #: Character length and limitations:
    #:     255 single-byte characters
    ebayitemauctiontxnid = core.StringField(max_length=255)

    #: Unique identifier of the specific payment request. The value should
    #: match the one you passed in the ``DoExpressCheckout`` request. You can
    #: specify up to 10 payments, where n is a digit between 0 and 9,
    #: inclusive.
    #:
    #:
    #: Character length and limitations:
    #:     Up to 127 single-byte characters
    paymentrequestid = core.StringField(max_length=127)


class Response(BaseType):
    """DoExpressCheckout Response Type."""
    #: The timestamped token value that was returned by ``SetExpressCheckout``
    #: response and passed on ``GetExpressCheckoutDetails`` request.
    #:
    #:
    #: Character length and limitations:
    #:     20 single-byte characters
    token = core.StringField(max_length=20)

    #: Information about the payment.
    paymenttype = core.StringField()

    #: The text entered by the buyer on the PayPal website if you set the
    #: ``ALLOWNOTE`` field to ``1`` in ``SetExpressCheckout``.
    #:
    #:
    #: Character length and limitations:
    #:     255 single-byte characters
    #:
    #:
    #: Available since API version: 53.0
    note = core.StringField()

    #: Flag to indicate whether you need to redirect the buyer back to PayPal
    #: after successfully completing the transaction.
    #:
    #:
    #: Notes:
    #:     Use this field only if you are using giropay or bank transfer
    #:     payment methods in Germany.
    redirectrequired = core.BooleanField()

    #: Flag to indicate whether you would like to redirect the buyer to sign
    #: up for
    #:
    #: PayPal after completing the transaction.
    successpageredirectrequested = core.BooleanField()

    #: The ID of the billing agreement associated with the Express Checkout
    #: transaction.
    billingagreementid = core.StringField()

    #: Store ID as entered in the transaction
    storeid = core.StringField()

    #: Terminal ID as entered in the transaction
    terminalid = core.StringField()

    #: List of ``PaymentInfo`` instances
    paymentinfo = core.ListTypeField(instanceof=PaymentInfo,
                                     required=True)
