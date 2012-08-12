# -*- coding: utf-8 -*-

from paypal.types import core
from paypal import countries, currencies, util


###############################################################################
# VALIDATORS
###############################################################################

def validate_survey_choice(choice):
    if len(choice) <= 15:
        return True

    message = 'Survey answer choice can at most be 15 characters long: %s'
    raise ValueError(message % choice)


###############################################################################
# EXPRESS CHECKOUT TYPE MIXINS
###############################################################################

class AddressMixin(core.BaseType):
    #: Person’s name associated with this shipping address.
    #:
    #: It is required if using a shipping address.
    #:
    #: Character length and limitations::
    #:     32 single-byte characters
    shiptoname = core.StringField(max_length=32)

    #: First street address.
    #:
    #: It is required if using a shipping address.
    #:
    #: Character length and limitations:
    #:     300 single-byte characters
    shiptostreet = core.StringField(max_length=300)

    #: Second street address.
    #:
    #: Character length and limitations:
    #:     300 single-byte characters
    shiptostreet2 = core.StringField(max_length=300)

    #: Name of city.
    #:
    #: It is required if using a shipping address.
    #:
    #: Character length and limitations::
    #:     40 single-byte characters
    shiptocity = core.StringField(max_length=40)

    #: State or province.
    #:
    #: It is required if using a shipping address.
    #:
    #: Character length and limitations::
    #:     40 single-byte characters
    shiptostate = core.StringField(max_length=40)

    #: U.S. ZIP code or other country-specific postal code.
    #:
    #: It is required if using a U.S. shipping address and may be required
    #: for other countries.
    #:
    #: Character length and limitations::
    #:     20 single-byte characters
    shiptozip = core.StringField(max_length=20)

    #: Country code.
    #:
    #: It is required if using a shipping address.
    #:
    #: Character length and limitations::
    #:     2 single-byte characters
    shiptocountrycode = core.StringField(length=2, choices=countries.codes)

    #: Phone number.
    #:
    #: Character length and limitations::
    #:     20 single-byte characters
    shiptophonenum = core.StringField(max_length=20)

    def validate_address(self):
        if not self.shiptoname:
            message = 'Using shipping address: shiptoname is required'
            raise ValueError(message)

        if not self.shiptostreet:
            message = 'Using shipping address: shiptostreet is required'
            raise ValueError(message)

        if not self.shiptocity:
            message = 'Using shipping address: shiptocity is required'
            raise ValueError(message)

        if not self.shiptocountrycode:
            message = 'Using shipping address: shiptocountrycode is required'
            raise ValueError(message)

        if not self.shiptozip and self.shiptocountrycode == 'US':
            message = 'Using shipping address: shiptozip is required within US'
            raise ValueError(message)

        return True


class PaymentDetailsMixin(core.BaseType):
    #: Total cost of the transaction to the buyer.
    #:
    #: If shipping cost and tax charges are known, include them in this value.
    #: If not, this value should be the current sub-total of the order.
    #: If the transaction includes one or more one-time purchases, this field
    #: must be equal to the sum of the purchases. Set this field to 0 if
    #: the transaction does not include a one-time purchase such as when you
    #: set up a billing agreement for a recurring payment that is not
    #: immediately charged. When the field is set to 0, purchase-specific
    #: fields are ignored.
    #:
    #: Character length and limitations::
    #:     Value is a positive number which cannot exceed $10,000 USD in
    #:     any currency. It includes no currency symbol. It must have
    #:     2 decimal places, the decimal separator must be a period (.),
    #:     and the optional thousands separator must be a comma (,).
    amt = core.MoneyField()

    #: Currency code (default is USD)
    #:
    #: Character length and limitations::
    #:    A 3-character currency code
    currencycode = core.StringField(length=3, choices=currencies.codes)

    #: Sum of cost of all items in this order.
    #:
    #: For digital goods, this field is required.
    #:
    #: Character length and limitations::
    #:     Value is a positive number which cannot exceed $10,000 USD in
    #:     any currency. It includes no currency symbol. It must have 2
    #:     decimal places, the decimal separator must be a period (.),
    #:     and the optional thousands separator must be a comma (,).
    itemamt = core.MoneyField()

    #: Total shipping costs for this order.
    #:
    #: Character length and limitations::
    #:     Value is a positive number which cannot exceed $10,000 USD
    #:     in any currency. It includes no currency symbol. It must have
    #:     2 decimal places, the decimal separator must be a period (.),
    #:     and the optional thousands separator must be a comma (,).
    #:
    #: Note:
    #:     If you specify a value for PAYMENTREQUEST_n_SHIPPINGAMT, you must
    #:     also specify a value for PAYMENTREQUEST_n_ITEMAMT.
    shippingamt = core.MoneyField()

    #: Total shipping insurance costs for this order.
    #: The value must be a non-negative currency amount or null if
    #: insurance options are offered.
    #:
    #: Character length and limitations::
    #:     Value is a positive number which cannot exceed $10,000 USD
    #:     in any currency. It includes no currency symbol. It must have
    #:     2 decimal places, the decimal separator must be a period (.),
    #:     and the optional thousands separator must be a comma (,).
    insuranceamt = core.MoneyField()

    #: Shipping discount for this order, specified as a negative number
    #:
    #: Character length and limitations::
    #:     Value is a positive number which cannot exceed $10,000 USD
    #:     in any currency. It includes no currency symbol. It must have
    #:     2 decimal places, the decimal separator must be a period (.),
    #:     and the optional thousands separator must be a comma (,).
    shipdiscamt = core.MoneyField()

    #: Indicates whether insurance is available as an option the buyer
    #: can choose on the PayPal Review page.
    #:
    #: Is one of the following values::
    #:     true – The Insurance option displays the string 'Yes' and
    #:            the insurance amount. If true, the total shipping
    #:            insurance for this order must be a positive number.
    #:     false – The Insurance option displays 'No'.
    #:
    #: Although the value is intended as a boolean we cannot
    #: utilize the BooleanField here since the string representation
    #: of the boolean values do not conform with the ordinary convention
    #: of '1' or '0'.
    insuranceoptionoffered = core.StringField(choices=('true', 'false'))

    #: Total handling costs for this order.
    #:
    #: Character length and limitations::
    #:     Value is a positive number which cannot exceed $10,000 USD
    #:     in any currency. It includes no currency symbol. It must have
    #:     2 decimal places, the decimal separator must be a period (.),
    #:     and the optional thousands separator must be a comma (,).
    #:
    #: Note::
    #:     If you specify a value for PAYMENTREQUEST_n_HANDLINGAMT,
    #:     you must also specify a value for PAYMENTREQUEST_n_ITEMAMT.
    handlingamt = core.MoneyField()

    #: Sum of tax for all items in this order.
    #:
    #: Character length and limitations::
    #:     Value is a positive number which cannot exceed $10,000 USD
    #:     in any currency. It includes no currency symbol. It must have
    #:     2 decimal places, the decimal separator must be a period (.),
    #:     and the optional thousands separator must be a comma (,).
    #:
    #: Note::
    #:     PAYMENTREQUEST_n_TAXAMT is required if you
    #:     specify L_PAYMENTREQUEST_n_TAXAMTm
    taxamt = core.MoneyField()

    #: Description of items the buyer is purchasing.
    #:
    #: Character length and limitations::
    #:     127 single-byte alphanumeric characters
    #:
    #: Note::
    #:     The value you specify is available only if the transaction
    #:     includes a purchase. This field is ignored if you set up a
    #:     billing agreement for a recurring payment that is not
    #.     immediately charged.
    desc = core.StringField(max_length=127)

    def validate_payment_details(self):
        if not self.amt:
            message = 'amt is required in paymentrequest'
            raise ValueError(message)

        if self.shippingamt and self.itemamt is None:
            message = 'itemamt is required when specifying shippingamt'
            raise ValueError(message)

        if self.handlingamt and self.itemamt is None:
            message = 'itemamt is required when specifying handlingamt'
            raise ValueError(message)

        return True


###############################################################################
# EXPRESS CHECKOUT TYPES
###############################################################################

class BaseType(core.BaseType):
    """Base Express Checkout type."""


class PaymentRequestType(BaseType,
                         AddressMixin,
                         PaymentDetailsMixin):
    #: Indicates the type of transaction.
    #:
    #: It is one of the following values::
    #:     None – Transaction is not identified as a particular type.
    #:     Refund – Identifies the transaction as a refund.
    paymentreason = core.StringField(choices=('None', 'Refund'))

    def has_shipping(self):
        return False

    def validate(self):
        if not super(PaymentRequestType, self).validate():
            return False

        if not self.validate_payment_details():
            return False

        if self.has_shipping():
            return self.validate_address()
        return True


###############################################################################
# EXPRESS CHECKOUT REQUESTS
###############################################################################

class SetExpressCheckoutRequest(BaseType):
    """The payload corresponding to the API method ``SetExpressCheckout``."""
    #: The name of the API method this payload corresponds to.
    #: This value must be ``SetExpressCheckout``
    method = core.ConstantField(u'SetExpressCheckout')

    #: The expected maximum total amount of the complete order,
    #: including shipping cost and tax charges. If the transaction includes
    #: one or more one-time purchases, this field is ignored.
    #:
    #: For recurring payments, you should pass the expected average
    #: transaction amount (default 25.00). PayPal uses this value to
    #: validate the buyer’s funding source.
    #:
    #: Character length and limitations::
    #:     Value is a positive number which cannot exceed $10,000 USD
    #:     in any currency. It includes no currency symbol.
    #:     It must have 2 decimal places, the decimal separator must
    #:     be a period (.), and the optional thousands separator
    #:     must be a comma (,).
    #:
    #: Note::
    #:     This field is required when implementing the Instant Update API
    #:     callback. PayPal recommends that the maximum total amount be
    #:     slightly greater than the sum of the line-item order details,
    #.     tax, and the shipping options of greatest value.
    maxamt = core.MoneyField(unsigned=True)

    #: URL to which the buyer’s browser is returned after choosing to pay
    #: with PayPal. For digital goods, you must add JavaScript to this page
    #: to close the in-context experience.
    #:
    #: Note::
    #:     PayPal recommends that the value be the final review page on which
    #.     the buyer confirms the order and payment or billing agreement.
    #:     Character length and limitations: 2048 single-byte characters
    #:
    #:     Since the URLField is a subclass of ``paypal.types.UnicodeField``
    #:     the maximum limit can be exceeded in case multi-byte characters
    #:     are included. However, since the value is intended to be a valid
    #:     URL this should not be an issue.
    returnurl = core.URLField(required=True, max_length=2048)

    #: URL to which the buyer is returned if the buyer does not approve the
    #: use of PayPal to pay you. For digital goods, you must add JavaScript
    #: to this page to close the in-context experience.
    #:
    #: Note::
    #:     PayPal recommends that the value be the original page on which the
    #:     buyer chose to pay with PayPal or establish a billing agreement.
    #:     Character length and limitations: 2048 single-byte characters
    #:
    #:     Since the URLField is a subclass of ``paypal.types.UnicodeField``
    #:     the maximum limit can be exceeded in case multi-byte characters
    #:     are included. However, since the value is intended to be a valid
    #:     URL this should not be an issue.
    cancelurl = core.URLField(required=True, max_length=2048)

    #: URL to which the callback request from PayPal is sent.
    #: It must start with HTTPS for production integration.
    #: It can start with HTTPS or HTTP for sandbox testing.
    #:
    #: Character length and limitations::
    #:     1024 single-byte characters
    #:
    #:     Since the URLField is a subclass of ``paypal.types.UnicodeField``
    #:     the maximum limit can be exceeded in case multi-byte characters
    #:     are included. However, since the value is intended to be a valid
    #:     URL this should not be an issue.
    #:
    #: Note::
    #:     This field is available since API version 53.0.
    callback = core.URLField(max_length=2048)

    #: An override for you to request more or less time to be able to process
    #: the callback request and respond. The acceptable range for the
    #: override is 1 to 6 seconds. If you specify a value greater than 6,
    #: PayPal uses the default value of 3 seconds.
    #:
    #: Character length and limitations::
    #:     An integer between 1 and 6
    callbacktimeout = core.IntegerField(min=1, max=6)

    #: Indicates whether or not you require the buyer’s shipping address
    #: on file with PayPal be a confirmed address. For digital goods, this
    #: field is required, and you must set it to 0.
    #:
    #: It is one of the following values::
    #:     0 – You do not require the buyer’s shipping address
    #:         be a confirmed address.
    #:     1 – You require the buyer’s shipping address be a
    #:         confirmed address.
    #:
    #: Character length and limitations::
    #:     1 single-byte numeric character
    #:
    #: Note:
    #:     Setting this field overrides the setting you specified in your
    #:     Merchant Account Profile.
    reqconfirmshipping = core.BooleanField()

    #: Determines where or not PayPal displays shipping address fields on
    #: the PayPal pages. For digital goods, this field is required,
    #: and you must set it to 1.
    #:
    #: It is one of the following values::
    #:     0 – PayPal displays the shipping address on the PayPal pages.
    #:     1 – PayPal does not display shipping address fields whatsoever.
    #:     2 – If you do not pass the shipping address, PayPal obtains it
    #:         from the buyer’s account profile.
    #:
    #: Character length and limitations::
    #:     4 single-byte numeric character
    noshipping = core.IntegerField(unsigned=True, max=2)

    #: Enables the buyer to enter a note to the merchant on the PayPal page
    #: during checkout. The note is returned in the GetExpressCheckoutDetails
    #: response and the DoExpressCheckoutPayment response.
    #:
    #: It is one of the following values::
    #:     0 – The buyer is unable to enter a note to the merchant.
    #:     1 – The buyer is able to enter a note to the merchant.
    #:
    #: Character length and limitations::
    #:     1 single-byte numeric character
    #:
    #: Note::
    #:     This field is available since version 53.0.
    allownote = core.BooleanField()

    #: Determines whether or not the PayPal pages should display the shipping
    #: address set by you in this SetExpressCheckout request, not the
    #: shipping address on file with PayPal for this buyer.
    #: Displaying the PayPal street address on file does not allow the buyer
    #: to edit that address.
    #:
    #: It is one of the following values::
    #:     0 – The PayPal pages should not display the shipping address.
    #:     1 – The PayPal pages should display the shipping address.
    #:
    #: Character length and limitations::
    #:     1 single-byte numeric character
    addoverride = core.BooleanField()

    #: Version of the callback API. This field is required when implementing
    #: the Instant Update Callback API.
    #:
    #: Character length and limitations::
    #:     The version string must be set to 61.0 or newer.
    #:
    #: Note::
    #:     This field is available since version 61.0.
    callbackversion = core.StringField()

    #: Locale of pages displayed by PayPal during Express Checkout.
    #: In case no override value is given the default locale is US.
    #:
    #: Character length and limitations::
    #:     A value which is specified in ``paypal.countries.SUPPORTED_LOCALES``
    localecode = core.StringField(choices=countries.SUPPORTED_LOCALES)

    #: Name of the Custom Payment Page Style for payment pages associated
    #: with this button or link. It corresponds to the HTML variable
    #: page_style for customizing payment pages. It is the same name as
    #: the Page Style Name you chose to add or edit the page style in your
    #: PayPal Account profile.
    #:
    #: Character length and limitations::
    #:     30 single-byte alphabetic characters
    pagestyle = core.StringField(max_length=30)

    #: URL for the image you want to appear at the top left of the
    #: payment page. The image has a maximum size of 750 pixels wide by
    #: 90 pixels high. PayPal recommends that you provide an image that is
    #: stored on a secure (https) server.
    #: If you do not specify an image, the business name displays.
    #:
    #: Character length and limitations::
    #:     127 single-byte alphanumeric characters
    hdrimg = core.URLField(max_length=127)

    #: Sets the border color around the header of the payment page.
    #: The border is a 2-pixel perimeter around the header space,
    #: which is 750 pixels wide by 90 pixels high.
    #: By default, the color is black ('000000').
    #:
    #: Character length and limitations::
    #:     6-character HTML hexadecimal ASCII color code
    hdrbordercolor = core.StringField(length=6)

    #: Sets the background color for the header of the payment page.
    #: By default, the color is white ('FFFFFF').
    #:
    #: Character length and limitations::
    #:     6-character HTML hexadecimal ASCII color code
    hdrbackcolor = core.StringField(length=6)

    #: Sets the background color for the payment page.
    #: By default, the color is white ('FFFFFF').
    #:
    #: Character length and limitations::
    #:     6-character HTML hexadecimal ASCII color code
    payflowcolor = core.StringField(length=6)

    #: Email address of the buyer as entered during checkout.
    #: PayPal uses this value to pre-fill the PayPal membership
    #: sign-up portion on the PayPal pages.
    #:
    #: Character length and limitations::
    #:     127 single-byte alphanumeric characters
    email = core.StringField(length=127)

    #: Type of checkout flow.
    #:
    #: It is one of the following values::
    #:     Sole – Buyer does not need to create a PayPal account to
    #:            check out. This is referred to as PayPal Account Optional.
    #:     Mark – Buyer must have a PayPal account to check out.
    #:
    #: Note::
    #:     You can pass Mark to selectively override the
    #:     PayPal Account Optional setting if PayPal Account Optional is
    #:     turned on in your merchant account.
    #:     Passing Sole has no effect if PayPal Account Optional
    #:     is turned off in your account
    solutiontype = core.StringField(choices=('Sole', 'Mark'))

    #: Type of PayPal page to display.
    #:
    #: It is one of the following values::
    #:     Billing – Non-PayPal account
    #:     Login – PayPal account login
    landingpage = core.StringField(choices=('Billing', 'Login'))

    #: Type of channel.
    #:
    #: It is one of the following values::
    #:     Merchant – Non-auction seller
    #:     eBayItem – eBay auction
    channeltype = core.StringField(choices=('Merchant', 'eBayItem'))

    #: The URL on the merchant site to redirect to after
    #: a successful giropay payment.
    #:
    #: Note::
    #:     Use this field only if you are using giropay or
    #:     bank transfer payment methods in Germany.
    giropaysuccessurl = core.URLField()

    #: The URL on the merchant site to redirect to after
    #: a successful giropay payment.
    #:
    #: Note::
    #:     Use this field only if you are using giropay or
    #:     bank transfer payment methods in Germany.
    giropaycancelurl = core.URLField()

    #: The URL on the merchant site to transfer to after
    #: a bank transfer payment.
    #:
    #: Note::
    #:     Use this field only if you are using giropay or
    #:     bank transfer payment methods in Germany.
    banktxnpendingurl = core.URLField()

    #: A label that overrides the business name in the PayPal account
    #: on the PayPal hosted checkout pages.
    #:
    #: Character length and limitations::
    #:     127 single-byte alphanumeric characters
    brandname = core.StringField(max_length=127)

    #: Merchant Customer Service number displayed on the PayPal pages.
    #:
    #: Character length and limitations::
    #:     16 single-byte characters
    customerservicenumber = core.StringField(max_length=16)

    #: Enables the gift message widget on the PayPal pages.
    #:
    #: It is one of the following values::
    #:      0 – Do not enable gift message widget.
    #:      1 – Enable gift message widget.
    giftmessageenable = core.BooleanField()

    #: Enable gift receipt widget on the PayPal pages.
    #:
    #: It is one of the following values:
    #:     0 – Do not enable gift receipt widget.
    #:     1 – Enable gift receipt widget.
    giftreceiptenable = core.BooleanField()

    #: Enable gift wrap widget on the PayPal pages.
    #:
    #: It is one of the following values::
    #:     0 – Do not enable gift wrap widget.
    #:     1 – Enable gift wrap widget.
    #:
    #: Note::
    #:     If you pass the value 1 in this field, values for the gift
    #:     wrap amount and gift wrap name are not passed, the gift wrap
    #:     name is not displayed, and the gift wrap amount displays as 0.00.
    giftwrapenable = core.BooleanField()

    #: Label for the gift wrap option such as “Box with ribbon.”
    #:
    #: Character length and limitations::
    #:     25 single-byte characters
    giftwrapname = core.StringField()

    #: Amount to be charged to the buyer for gift wrapping.
    #:
    #: Character length and limitations::
    #:     Value is a positive number which cannot exceed $10,000 USD in
    #:     any currency. It includes no currency symbol.
    #:     It must have 2 decimal places, the decimal separator must be
    #:     a period (.), and the optional thousands separator must
    #:     be a comma (,).
    giftwrapamount = core.MoneyField()

    #: Enables the buyer to provide their email address on the PayPal pages
    #: to be notified of promotions or special events.
    #:
    #: Is one of the following values::
    #:     0 – Do not enable buyer to provide email address.
    #:     1 – Enable the buyer to provide email address.
    buyeremailoptinenable = core.BooleanField()

    #: Text for the survey question on the PayPal pages.
    #: If the survey question is present, at least 2 survey answer
    #: options must be present.
    #:
    #: Character length and limitations::
    #:     50 single-byte characters
    surveyquestion = core.StringField(max_length=50)

    #: Enables survey functionality.
    #:
    #: It is one of the following values::
    #:     0 – Disables survey functionality.
    #:     1 – Enables survey functionality.
    surveyenable = core.BooleanField()

    #: Possible options for the survey answers on the PayPal pages.
    #: Answers are displayed only if a valid survey question is present.
    #:
    #: Character length and limitations::
    #:     15 single-byte characters
    surveychoice = core.ListField(
        sanitization_callback=util.ensure_unicode,
        validation_callback=validate_survey_choice,
    )

    #: List of ``PaymentRequestType`` instances
    paymentrequest = core.ListTypeField(instanceof=PaymentRequestType,
                                        required=True)

    ###########################################################################
    # LOCAL SANITIZATION METHODS
    ###########################################################################

    def is_digital_goods(self):
        return False

    def has_instant_update_callback(self):
        return False

    def validate(self):
        if not super(SetExpressCheckoutRequest, self).validate():
            return False

        if self.has_instant_update_callback():
            self.validate_instant_update_requirements()

        if self.is_digital_goods():
            self.validate_digital_goods_requirements()
            if len(self.paymentrequest) > 1:
                message = 'Selling digital goods: multiple paymentrequests'
                raise ValueError(message)
        elif len(self.paymentrequest) > 10:
            message = 'Too many instances of paymentrequest. 10 is the limit.'
            raise ValueError(message)

        return True

    def validate_instant_update_requirements(self):
        if self.maxamt is None:
            msg = 'Using Instant Update API: maxamt is required'
            raise ValueError(msg)

        if self.callbackversion is None:
            msg = 'Using Instant Update API: callbackversion is required'
            raise ValueError(msg)

        callbackversion = float(self.callbackversion)
        if callbackversion < 61.0:
            msg = 'Using Instant Update API: callbackversion has to be >= 61.0'
            raise ValueError(msg)

        return True

    def validate_digital_goods_requirements(self):
        if self.reqconfirmshipping != 0:
            msg = 'Selling digital goods: reqconfirmshipping has to equal 0'
            raise ValueError(msg)

        if self.noshipping != 1:
            msg = 'Selling digital goods: noshipping has to equal 1'
            raise ValueError(msg)

        return True
