# -*- coding: utf-8 -*-

from paypal.types import core
from paypal import countries, currencies, util


###############################################################################
# VALIDATORS
###############################################################################

def validate_item_category(value):
    valid = set(['Digital', 'Physical'])
    if value in valid:
        return True

    message = 'Item category value is not one of %s: %s'
    raise ValueError(message % (valid, value))


###############################################################################
# MIXINS
###############################################################################

class AddressMixin(core.BaseType):
    """The params related to the buyers address."""
    #: Person’s name associated with this shipping address. It is required if
    #: using a shipping address. You can specify up to 10 payments, where n is
    #: a digit between 0 and 9, inclusive.
    #:
    #:
    #: Character length and limitations:
    #:     32 single-byte characters
    shiptoname = core.StringField(max_length=32)

    #: First street address. It is required if using a shipping address. You
    #: can specify up to 10 payments, where n is a digit between 0 and 9,
    #: inclusive.
    #:
    #:
    #: Character length and limitations:
    #:     300 single-byte characters
    shiptostreet = core.StringField(max_length=300)

    #: (Optional) Second street address. You can specify up to 10 payments,
    #: where n is a digit between 0 and 9, inclusive.
    #:
    #:
    #: Character length and limitations:
    #:     300 single-byte characters
    shiptostreet2 = core.StringField(max_length=300)

    #: Name of city. It is required if using a shipping address. You can
    #: specify up to 10 payments, where n is a digit between 0 and 9,
    #: inclusive.
    #:
    #:
    #: Character length and limitations:
    #:     40 single-byte characters
    shiptocity = core.StringField(max_length=40)

    #: State or province. It is required if using a shipping address. You can
    #: specify up to 10 payments, where n is a digit between 0 and 9,
    #: inclusive.
    #:
    #:
    #: Character length and limitations:
    #:     40 single-byte characters
    shiptostate = core.StringField(max_length=40)

    #: U.S. ZIP code or other country-specific postal code. It is required if
    #: using a U.S. shipping address and may be required for other countries.
    #: You can specify up to 10 payments, where n is a digit between 0 and 9,
    #: inclusive.
    #:
    #:
    #: Character length and limitations:
    #:     20 single-byte characters
    shiptozip = core.StringField(max_length=20)

    #: Country code. It is required if using a shipping address. You can
    #: specify up to 10 payments, where n is a digit between 0 and 9,
    #: inclusive.
    #:
    #:
    #: Character length and limitations:
    #:     2 single-byte characters
    shiptocountrycode = core.StringField(length=2, choices=countries.codes)

    #: (Optional) Phone number. You can specify up to 10 payments, where n is
    #: a digit between 0 and 9, inclusive.
    #:
    #:
    #: Character length and limitations:
    #:     20 single-byte characters
    shiptophonenum = core.StringField(max_length=20)


class PaymentDetailsMixin(core.BaseType):
    """The params related to the details."""
    #: (Required) Total cost of the transaction to the buyer. If shipping cost
    #: and tax charges are known, include them in this value. If not, this
    #: value should be the current sub-total of the order. If the transaction
    #: includes one or more one-time purchases, this field must be equal to
    #: the sum of the purchases. Set this field to 0 if the transaction does
    #: not include a one-time purchase such as when you set up a billing
    #: agreement for a recurring payment that is not immediately charged. When
    #: the field is set to 0, purchase-specific fields are ignored. You can
    #: specify up to 10 payments, where n is a digit between 0 and 9,
    #: inclusive; except for digital goods, which supports single payments
    #: only.
    #:
    #:
    #: Character length and limitations:
    #:     Value is a positive number which cannot exceed $10,000 USD in any
    #:     currency. It includes no currency symbol. It must have 2 decimal
    #:     places, the decimal separator must be a period (.), and the
    #:     optional thousands separator must be a comma (,).
    amt = core.MoneyField()

    #: (Optional) A 3-character currency code (default is USD). You can
    #: specify up to 10 payments, where n is a digit between 0 and 9,
    #: inclusive; except for digital goods, which supports single payments
    #: only.
    currencycode = core.StringField(length=3, choices=currencies.codes)

    #: Sum of cost of all items in this order. For digital goods, this field
    #: is required. You can specify up to 10 payments, where n is a digit
    #: between 0 and 9, inclusive; except for digital goods, which supports
    #: single payments only.
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
    #:     ``PAYMENTREQUEST_n_ITEMAMT`` is required if you specify
    #:     ``L_PAYMENTREQUEST_n_AMTm``.
    itemamt = core.MoneyField()

    #: (Optional) Total shipping costs for this order. You can specify up to
    #: 10 payments, where n is a digit between 0 and 9, inclusive.
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
    #:     If you specify a value for ``PAYMENTREQUEST_n_SHIPPINGAMT``, you
    #:     must also specify a value for ``PAYMENTREQUEST_n_ITEMAMT``.
    shippingamt = core.MoneyField()

    #: (Optional) Total shipping insurance costs for this order. The value
    #: must be a non-negative currency amount or ``null`` if insurance options
    #: are offered. You can specify up to 10 payments, where n is a digit
    #: between 0 and 9, inclusive.
    #:
    #:
    #: Character length and limitations:
    #:     Value is a positive number which cannot exceed $10,000 USD in any
    #:     currency. It includes no currency symbol. It must have 2 decimal
    #:     places, the decimal separator must be a period (.), and the
    #:     optional thousands separator must be a comma (,).
    insuranceamt = core.MoneyField()

    #: (Optional) Shipping discount for this order, specified as a negative
    #: number. You can specify up to 10 payments, where n is a digit between 0
    #: and 9, inclusive.
    #:
    #:
    #: Character length and limitations:
    #:     Value is a positive number which cannot exceed $10,000 USD in any
    #:     currency. It includes no currency symbol. It must have 2 decimal
    #:     places, the decimal separator must be a period (.), and the
    #:     optional thousands separator must be a comma (,).
    shipdiscamt = core.MoneyField()

    #: (Optional) Indicates whether insurance is available as an option the
    #: buyer can choose on the PayPal Review page. You can specify up to 10
    #: payments, where n is a digit between 0 and 9, inclusive. Is one of the
    #: following values:
    #:
    #:     ``true`` – The Insurance option displays the string ``'Yes'`` and
    #:     the insurance amount. If ``true``, the total shipping insurance for
    #:     this order must be a positive number.
    #:
    #:     ``false`` – The Insurance option displays ``'No'``.
    insuranceoptionoffered = core.StringField(choices=('true', 'false'))

    #: (Optional) Total handling costs for this order. You can specify up to
    #: 10 payments, where n is a digit between 0 and 9, inclusive.
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
    #:     If you specify a value for ``PAYMENTREQUEST_n_HANDLINGAMT``, you
    #:     must also specify a value for ``PAYMENTREQUEST_n_ITEMAMT``.
    handlingamt = core.MoneyField()

    #: (Optional) Sum of tax for all items in this order. You can specify up
    #: to 10 payments, where n is a digit between 0 and 9, inclusive; except
    #: for digital goods, which supports single payments only.
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
    #:     ``PAYMENTREQUEST_n_TAXAMT`` is required if you specify
    #:     ``L_PAYMENTREQUEST_n_TAXAMTm``
    taxamt = core.MoneyField()

    #: (Optional) Description of items the buyer is purchasing. You can
    #: specify up to 10 payments, where n is a digit between 0 and 9,
    #: inclusive; except for digital goods, which supports single payments
    #: only.
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

    #: (Optional) A free-form field for your own use. You can specify up to 10
    #: payments, where n is a digit between 0 and 9, inclusive.
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

    #: (Optional) Your own invoice or tracking number.You can specify up to 10
    #: payments, where n is a digit between 0 and 9, inclusive; except for
    #: digital goods, which supports single payments only.
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

    #: (Optional) Your URL for receiving Instant Payment Notification (IPN)
    #: about this transaction. If you do not specify this value in the
    #: request, the notification URL from your Merchant Profile is used, if
    #: one exists.You can specify up to 10 payments, where n is a digit
    #: between 0 and 9, inclusive; except for digital goods, which supports
    #: single payments only.
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

    #: (Optional) Note to the merchant. You can specify up to 10 payments,
    #: where n is a digit between 0 and 9, inclusive.
    #:
    #:
    #: Character length and limitations:
    #:     255 single-byte characters
    notetext = core.StringField(max_length=255)

    #: (Optional) Transaction identification number of the transaction that
    #: was created. You can specify up to 10 payments, where n is a digit
    #: between 0 and 9, inclusive.
    #:
    #:
    #: Notes:
    #:     This field is only returned after a successful transaction for
    #:     ``DoExpressCheckout`` has occurred.
    transactionid = core.IntegerField()

    #: (Optional) The payment method type. Specify the value
    #: ``InstantPaymentOnly``. You can specify up to 10 payments, where n is a
    #: digit between 0 and 9, inclusive.
    allowedpaymentmethod = core.StringField()

    #: A unique identifier of the specific payment request, which is required
    #: for parallel payments. You can specify up to 10 payments, where n is a
    #: digit between 0 and 9, inclusive.
    #:
    #:
    #: Character length and limitations:
    #:     Up to 127 single-byte characters
    paymentrequestid = core.StringField(max_length=127)


class PaymentDetailsWithActionMixin(PaymentDetailsMixin):
    """The params related to the details, but with payment action as well."""
    #: How you want to obtain payment. When implementing parallel payments,
    #: this field is required and must be set to ``Order``. When implementing
    #: digital goods, this field is required and must be set to ``Sale``. You
    #: can specify up to 10 payments, where n is a digit between 0 and 9,
    #: inclusive; except for digital goods, which supports single payments
    #: only. If the transaction does not include a one-time purchase, this
    #: field is ignored. It is one of the following values:
    #:
    #:
    #:     ``Sale`` – This is a final sale for which you are requesting
    #:     payment (default).
    #:
    #:     ``Authorization`` – This payment is a basic authorization subject
    #:     to settlement with PayPal Authorization and Capture.
    #:
    #:     ``Order`` – This payment is an order authorization subject to
    #:     settlement with PayPal Authorization and Capture.
    #:
    #:
    #: Character length and limitations:
    #:     Up to 13 single-byte alphabetic characters
    #:
    #:
    #: Notes:
    #:     You cannot set this field to ``Sale`` in ``SetExpressCheckout``
    #:     request and then change the value to ``Authorization`` or ``Order``
    #:     in the ``DoExpressCheckoutPayment`` request. If you set the field
    #:     to ``Authorization`` or ``Order`` in ``SetExpressCheckout``, you
    #:     may set the field to ``Sale``.
    paymentaction = core.StringField(
        choices=('Sale', 'Authorization', 'Order'),
    )


class PaymentItemDetailsMixin(core.BaseType):
    """The params related to the item details."""
    #: Item name. This field is required when
    #: ``L_PAYMENTREQUEST_n_ITEMCATEGORYm`` is passed. You can specify up to
    #: 10 payments, where n is a digit between 0 and 9, inclusive, and m
    #: specifies the list item within the payment; except for digital goods,
    #: which supports single payments only. These parameters must be ordered
    #: sequentially beginning with 0 (for example
    #: ``L_PAYMENTREQUEST_n_NAME0``, ``L_PAYMENTREQUEST_n_NAME1``).
    #:
    #:
    #: Character length and limitations:
    #:     127 single-byte characters
    name = core.ListStringField(
        validation_callback=core.gen_strlen_validator('name', 127),
    )

    #: (Optional) Item description. You can specify up to 10 payments, where n
    #: is a digit between 0 and 9, inclusive, and m specifies the list item
    #: within the payment; except for digital goods, which supports single
    #: payments only. These parameters must be ordered sequentially beginning
    #: with 0 (for example ``L_PAYMENTREQUEST_n_DESC0``,
    #: ``L_PAYMENTREQUEST_n_DESC1``).
    #:
    #:
    #: Character length and limitations:
    #:     127 single-byte characters
    desc = core.ListStringField(
        validation_callback=core.gen_strlen_validator('desc', 127),
    )

    #: Cost of item. This field is required when
    #: ``L_PAYMENTREQUEST_n_ITEMCATEGORYm`` is passed. You can specify up to 10
    #: payments, where n is a digit between 0 and 9, inclusive, and m
    #: specifies the list item within the payment; except for digital goods,
    #: which supports single payments only. These parameters must be ordered
    #: sequentially beginning with 0 (for example ``L_PAYMENTREQUEST_n_AMT0``,
    #: ``L_PAYMENTREQUEST_n_AMT1``).
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
    #:     If you specify a value for ``L_PAYMENTREQUEST_n_AMTm``, you must
    #:     specify a value for ``PAYMENTREQUEST_n_ITEMAMT``.
    amt = core.ListField(sanitization_callback=core.Money)

    #: (Optional) Item number. You can specify up to 10 payments, where n is a
    #: digit between 0 and 9, inclusive, and m specifies the list item within
    #: the payment. These parameters must be ordered sequentially beginning
    #: with 0 (for example ``L_PAYMENTREQUEST_n_NUMBER0``,
    #: ``L_PAYMENTREQUEST_n_NUMBER1``).
    #:
    #:
    #: Character length and limitations:
    #:     127 single-byte characters
    number = core.ListStringField(
        validation_callback=core.gen_strlen_validator('number', 127),
    )

    #: Item quantity. This field is required when
    #: ``L_PAYMENTREQUEST_n_ITEMCATEGORYm`` is passed. For digital goods
    #: (``L_PAYMENTREQUEST_n_ITEMCATEGORYm=Digital``), this field is required.
    #: You can specify up to 10 payments, where n is a digit between 0 and 9,
    #: inclusive, and m specifies the list item within the payment; except for
    #: digital goods, which only supports single payments. These parameters
    #: must be ordered sequentially beginning with 0 (for example
    #: ``L_PAYMENTREQUEST_n_QTY0``, ``L_PAYMENTREQUEST_n_QTY1``).
    #:
    #: This field is introduced in version 53.0. ``L_QTYn`` is deprecated
    #: since version 63.0. Use ``L_PAYMENTREQUEST_0_QTYm`` instead.
    #:
    #:
    #: Character length and limitations:
    #:     Any positive integer
    qty = core.ListField(
        sanitization_callback=int,
        validation_callback=core.gen_unsigned_int_validator('qty'),
    )

    #: (Optional) Item sales tax. You can specify up to 10 payments, where n
    #: is a digit between 0 and 9, inclusive, and m specifies the list item
    #: within the payment; except for digital goods, which only supports
    #: single payments. These parameters must be ordered sequentially
    #: beginning with 0 (for example ``L_PAYMENTREQUEST_n_TAXAMT0``,
    #: ``L_PAYMENTREQUEST_n_TAXAMT1``).
    #:
    #:
    #: Character length and limitations:
    #:     Value is a positive number which cannot exceed $10,000 USD in any
    #:     currency. It includes no currency symbol. It must have 2 decimal
    #:     places, the decimal separator must be a period (.), and the
    #:     optional thousands separator must be a comma (,).
    taxamt = core.ListField(sanitization_callback=core.Money)


    #: (Optional) Item weight corresponds to the weight of the item. You can
    #: pass this data to the shipping carrier as is without having to make an
    #: additional database query. You can specify up to 10 payments, where n
    #: is a digit between 0 and 9, inclusive, and m specifies the list item
    #: within the payment;. These parameters must be ordered sequentially
    #: beginning with 0 (for example ``L_PAYMENTREQUEST_n_ITEMWEIGHTVALUE0``,
    #: ``L_PAYMENTREQUEST_n_ITEMWEIGHTVALUE1``).
    #:
    #:
    #: Character length and limitations:
    #:     Any positive integer
    itemweightvalue = core.ListField(
        sanitization_callback=int,
        validation_callback=core.gen_unsigned_int_validator('itemweightvalue'),
    )

    #: (Optional) Item length corresponds to the length of the item. You can
    #: pass this data to the shipping carrier as is without having to make an
    #: additional database query. You can specify up to 10 payments, where n
    #: is a digit between 0 and 9, inclusive, and m specifies the list item
    #: within the payment. These parameters must be ordered sequentially
    #: beginning with 0 (for example ``L_PAYMENTREQUEST_n_ITEMLENGTHVALUE0``,
    #: ``L_PAYMENTREQUEST_n_ITEMLENGTHVALUE1``).
    #:
    #:
    #: Character length and limitations:
    #:     Any positive integer
    itemlengthvalue = core.ListField(
        sanitization_callback=int,
        validation_callback=core.gen_unsigned_int_validator('itemlengthvalue'),
    )

    #: (Optional) Item width corresponds to the width of the item. You can
    #: pass this data to the shipping carrier as is without having to make an
    #: additional database query. You can specify up to 10 payments, where n
    #: is a digit between 0 and 9, inclusive, and m specifies the list item
    #: within the payment. These parameters must be ordered sequentially
    #: beginning with 0 (for example ``L_PAYMENTREQUEST_n_ITEMWIDTHVALUE0``,
    #: ``L_PAYMENTREQUEST_n_ITEMWIDTHVALUE1``).
    #:
    #:
    #: Character length and limitations:
    #:     Any positive integer
    itemwidthvalue = core.ListField(
        sanitization_callback=int,
        validation_callback=core.gen_unsigned_int_validator('itemwidthvalue'),
    )

    #: (Optional) Item height corresponds to the height of the item. You can
    #: pass this data to the shipping carrier as is without having to make an
    #: additional database query. You can specify up to 10 payments, where n
    #: is a digit between 0 and 9, inclusive, and m specifies the list item
    #: within the payment. These parameters must be ordered sequentially
    #: beginning with 0 (for example ``L_PAYMENTREQUEST_n_ITEMHEIGHTVALUE0``,
    #: ``L_PAYMENTREQUEST_n_ITEMHEIGHTVALUE1``).
    #:
    #:
    #: Character length and limitations:
    #:     Any positive integer
    itemheightvalue = core.ListField(
        sanitization_callback=int,
        validation_callback=core.gen_unsigned_int_validator('itemheightvalue'),
    )

    #: Indicates whether an item is digital or physical. For digital goods,
    #: this field is required and must be set to ``Digital``. You can specify
    #: up to 10 payments, where n is a digit between 0 and 9, inclusive, and m
    #: specifies the list item within the payment; except for digital goods,
    #: which only supports single payments. These parameters must be ordered
    #: sequentially beginning with 0 (for example
    #: ``L_PAYMENTREQUEST_n_ITEMCATEGORY0``,
    #: ``L_PAYMENTREQUEST_n_ITEMCATEGORY1``). It is one of the following
    #: values:
    #:
    #:     ``Digital``
    #:
    #:     ``Physical``
    #:
    #:
    #: Available since API version: 65.1
    itemcategory = core.ListField(
        sanitization_callback=util.ensure_unicode,
        validation_callback=validate_item_category,
    )


class PaymentItemDetailsWithURLMixin(core.BaseType):
    """The params related to the item details, but with item URL as well."""
    #: (Optional) URL for the item. You can specify up to 10 payments, where n
    #: is a digit between 0 and 9, inclusive, and m specifies the list item
    #: within the payment. These parameters must be ordered sequentially
    #: beginning with 0 (for example ``L_PAYMENTREQUEST_n_ITEMURL0``,
    #: ``L_PAYMENTREQUEST_n_ITEMURL1``).
    itemurl = core.ListField(sanitization_callback=util.ensure_unicode)


class eBayPaymentDetailsMixin(core.BaseType):
    """The params related to the eBay details."""
    #: (Optional) Auction item number. You can specify up to 10 payments,
    #: where n is a digit between 0 and 9, inclusive, and m specifies the list
    #: item within the payment. These parameters must be ordered sequentially
    #: beginning with 0 (for example ``L_PAYMENTREQUEST_n_EBAYITEMNUMBER0``,
    #: ``L_PAYMENTREQUEST_n_EBAYITEMNUMBER1``).
    #:
    #: Character length: 765 single-byte characters
    ebayitemnumber = core.ListStringField(
        validation_callback=core.gen_strlen_validator('ebayitemnumber', 765),
    )

    #: (Optional) Auction transaction identification number. You can specify
    #: up to 10 payments, where n is a digit between 0 and 9, inclusive, and m
    #: specifies the list item within the payment. These parameters must be
    #: ordered sequentially beginning with 0 (for example
    #: ``L_PAYMENTREQUEST_n_EBAYITEMAUCTIONTXNID0``,
    #: ``L_PAYMENTREQUEST_n_EBAYITEMAUCTIONTXNID1``).
    #:
    #: Character length: 255 single-byte characters
    ebayitemauctiontxnid = core.ListStringField(
        validation_callback=core.gen_strlen_validator(
            'ebayitemauctiontxnid', 255,
        ),
    )

    #: (Optional) Auction order identification number. You can specify up to
    #: 10 payments, where n is a digit between 0 and 9, inclusive, and m
    #: specifies the list item within the payment. These parameters must be
    #: ordered sequentially beginning with 0 (for example
    #: ``L_PAYMENTREQUEST_n_EBAYITEMORDERID0``,
    #: ``L_PAYMENTREQUEST_n_EBAYITEMORDERID1``).
    #:
    #: Character length: 64 single-byte characters
    ebayitemorderid = core.ListStringField(
        validation_callback=core.gen_strlen_validator('ebayitemorderid', 64),
    )

    #: (Optional) The unique identifier provided by eBay for this order from
    #: the buyer. You can specify up to 10 payments, where n is a digit
    #: between 0 and 9, inclusive, and m specifies the list item within the
    #: payment. These parameters must be ordered sequentially beginning with 0
    #: (for example ``L_PAYMENTREQUEST_n_EBAYITEMCARTID0``,
    #: ``L_PAYMENTREQUEST_n_EBAYITEMCARTID1``).
    #:
    #: Character length: 255 single-byte characters
    ebaycartid = core.ListStringField(
        validation_callback=core.gen_strlen_validator('ebaycartid', 255),
    )


class SellerDetailsMixin(core.BaseType):
    """The params related to the seller details."""
    #: Unique identifier for the merchant. For parallel payments, this field
    #: is required and must contain the Payer ID or the email address of the
    #: merchant. You can specify up to 10 payments, where n is a digit between
    #: 0 and 9, inclusive.
    #:
    #:
    #: Character length and limitations:
    #:     127 single-byte alphanumeric characters
    sellerpaypalaccountid = core.StringField(max_length=127)


class SellerDetailsWithMerchantAccountMixin(SellerDetailsMixin):
    """The params related to the seller details along with
    the merchant account identifier.

    """
    #: Unique PayPal customer account number (of the merchant). This field is
    #: returned in the response. It is ignored if passed in the request.
    securemerchantaccountid = core.StringField()


class TaxDetailsMixin(core.BaseType):
    """The params related to the tax details."""
    #: Buyer’s tax ID type. This field is required for Brazil and used for
    #: Brazil only.
    #:
    #: For Brazil use only: The tax ID type is ``BR_CPF`` for individuals and
    #: ``BR_CNPJ`` for businesses.
    #:
    #:
    #: Available since API version: 72.0
    taxidtype = core.StringField(choices=('BR_CPF', 'BR_CPNJ'))

    #: Buyer’s tax ID. This field is required for Brazil and used for Brazil
    #: only.
    #:
    #: For Brazil use only: The tax ID is 11 single-byte characters for
    #: individuals and 14 single-byte characters for businesses.
    #:
    #:
    #: Available since API version: 72.0
    taxiddetails = core.StringField(max_length=14)


class UserSelectedOptionsMixin(core.BaseType):
    """The params related to the user selected payment options."""
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


class UserSelectedOptionsWithCalculationMixin(UserSelectedOptionsMixin):
    """The params related to the user selected payment options
    along with the shipping calculation mode.

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


###############################################################################
# TYPES
###############################################################################

class BaseType(core.BaseType):
    """Base Express Checkout Type."""


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


class PaymentRequest(BaseType,
                     AddressMixin,
                     PaymentDetailsMixin,
                     PaymentItemDetailsMixin,
                     eBayPaymentDetailsMixin):
    """Payment Request Package."""
