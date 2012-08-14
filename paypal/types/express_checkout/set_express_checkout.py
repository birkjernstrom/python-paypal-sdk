# -*- coding: utf-8 -*-

from paypal.types import core
from paypal.types.express_checkout import base
from paypal import countries


###############################################################################
# MIXINS
###############################################################################

#: Alias for ``base.PaymentDetailsWithMixin``
PaymentDetailsWithActionMixin = base.PaymentDetailsWithActionMixin
#: Alias for ``base.PaymentItemURLDetailsMixin``
PaymentItemURLDetailsMixin = base.PaymentItemURLDetailsMixin
#: Alias for ``base.PaymentItemDimensionDetailsMixin``
PaymentItemDimensionDetailsMixin = base.PaymentItemDimensionDetailsMixin
#: Alias for ``base.TaxDetailsMixin``
TaxDetailsMixin = base.TaxDetailsMixin
#: Alias for ``base.eBayPaymentCartDetailsMixin``
eBayPaymentCartDetailsMixin = base.eBayPaymentCartDetailsMixin
#: Alias for ``base.SellerDetailsMixin``
SellerDetailsMixin = base.SellerDetailsMixin


class BuyerDetailsMixin(core.BaseType):
    """The params related to the buyer details of a ``Request``."""
    #: (Optional) The unique identifier provided by eBay for this buyer. The
    #: value may or may not be the same as the username. In the case of eBay,
    #: it is different.
    #:
    #:
    #: Character length and limitations:
    #:     255 single-byte characters
    buyerid = core.StringField(max_length=255)

    #: (Optional) The user name of the user at the marketplaces site.
    buyerusername = core.StringField()

    #: (Optional) Date when the user registered with the marketplace.
    #:
    #:
    #: Character length and limitations:
    #:     Date and time are in UTC/GMT format, for example,
    #:     ``2011-06-24T05:38:48Z``
    buyerregistrationdate = core.UTCDatetimeField()


class FundingSourceDetailsMixin(core.BaseType):
    """The params related to the funding source details of a ``Request``."""
    #: (Optional) Indicates whether the merchant can accept push funding. It
    #: is one of the following values:
    #:
    #:     ``0`` – Merchant can accept push funding.
    #:
    #:     ``1`` – Merchant cannot accept push funding.
    #:
    #:
    #: Notes:
    #:     This field overrides the setting in the merchant's PayPal account.
    allowpushfunding = core.BooleanField()


class ShippingOptionsMixin(core.BaseType):
    """The params related to the shipping option details of a ``Request``."""
    #: Default shipping option displayed on the PayPal pages. This field is
    #: required if you specify the Callback URL. It is one of the following
    #: values:
    #:
    #:
    #:     ``true`` – This is the default flat-rate shipping option. PayPal
    #:     displays this option and its amount by default.
    #:
    #:     ``false`` – This flat-rate shipping option and its amount are not
    #:     displayed as the default.
    #:
    #:
    #: Notes:
    #:     There must be ONE and ONLY ONE default. It is not OK to have no
    #:     default.
    shippingoptionisdefault = core.ListStringField(
        validation_callback=core.gen_choice_validator(
            'shippingoptionisdefault',
            ('true', 'false'),
        ),
    )

    #: Internal name of the shipping option such as Air, Ground, Expedited,
    #: and so forth. This field is required if you specify the Callback URL.
    #:
    #:
    #: Character length and limitations:
    #:     50 character-string.
    shippingoptionname = core.ListStringField(
        validation_callback=core.gen_strlen_validator(
            'shippingoptionname', 50,
        ),
    )

    #: Amount of the flat rate shipping option. This field is required if you
    #: specify the Callback URL.
    #:
    #:
    #: Character length and limitations:
    #:     Value is a positive number which cannot exceed $10,000 USD in any
    #:     currency. It includes no currency symbol. It must have 2 decimal
    #:     places, the decimal separator must be a period (.), and the
    #:     optional thousands separator must be a comma (,).
    shippingoptionamount = core.ListField(sanitization_callback=core.Money)


class BillingAgreementDetailsMixin(core.BaseType):
    """The params related to the billing agreement details of a ``Request``."""
    #: (Required) Type of billing agreement. For recurring payments, this
    #: field must be set to ``RecurringPayments``. In this case, you can
    #: specify up to ten billing agreements. Other defined values are not
    #: valid.
    #:
    #: Type of billing agreement for reference transactions. You must have
    #: permission from PayPal to use this field. This field must be set to one
    #: of the following values:
    #:
    #:     ``MerchantInitiatedBilling`` - PayPal creates a billing agreement
    #:     for each transaction associated with buyer. You must specify
    #:     version 54.0 or higher to use this option.
    #:
    #:     ``MerchantInitiatedBillingSingleAgreement`` - PayPal creates a
    #:     single billing agreement for all transactions associated with
    #:     buyer. Use this value unless you need per-transaction billing
    #:     agreements. You must specify version 58.0 or higher to use this
    #:     option.
    billingtype = core.ListStringField(
        validation_callback=core.gen_choice_validator(
            'MerchantInitiatedBilling',
            'MerchantInitiatedBillingSingleAgreement',
        ),
    )

    #: Description of goods or services associated with the billing agreement.
    #: This field is required for each recurring payment billing agreement.
    #: PayPal recommends that the description contain a brief summary of the
    #: billing agreement terms and conditions. For example, buyer is billed at
    #: “9.99 per month for 2 years”.
    #:
    #:
    #: Character length and limitations:
    #:     127 single-byte alphanumeric characters
    billingagreementdescription = core.ListStringField(
        validation_callback=core.gen_strlen_validator(
            'billingagreementdescription', 127,
        ),
    )

    #: (Optional) Type of PayPal payment you require for the billing
    #: agreement. It is one of the following values:
    #:
    #:     ``Any``
    #:
    #:     ``InstantOnly``
    #:
    #:
    #: Notes:
    #:     For recurring payments, this field is ignored.
    paymenttype = core.ListStringField(
        validation_callback=core.gen_choice_validator(
            'paymenttype',
            ('Any', 'InstantOnly'),
        ),
    )

    #: (Optional) Custom annotation field for your own use.
    #:
    #:
    #: Character length and limitations:
    #:     256 single-byte alphanumeric bytes
    #:
    #:
    #: Notes:
    #:     For recurring payments, this field is ignored.
    billingagreementcustom = core.ListStringField(
        validation_callback=core.gen_strlen_validator(
            'billingagreementcustom', 256,
        ),
    )


###############################################################################
# TYPES
###############################################################################

#: Alias for ``base.BaseType``
BaseType = base.BaseType


class PaymentRequest(base.PaymentRequestWithReason,
                     PaymentDetailsWithActionMixin,
                     PaymentItemDimensionDetailsMixin,
                     PaymentItemURLDetailsMixin,
                     eBayPaymentCartDetailsMixin,
                     SellerDetailsMixin):
    """The Payment Request intended to be included in a
    SetExpressCheckout request, i.e it is not a standalone request
    but rather an integral part of the SetExpressCheckout call.

    """


class Request(core.Request,
              BuyerDetailsMixin,
              FundingSourceDetailsMixin,
              ShippingOptionsMixin,
              BillingAgreementDetailsMixin,
              TaxDetailsMixin):
    """SetExpressCheckout Request Type."""
    #: (Required) Must be SetExpressCheckout.
    method = core.ConstantField(u'SetExpressCheckout')

    #: (Optional) The expected maximum total amount of the complete order,
    #: including shipping cost and tax charges. If the transaction includes
    #: one or more one-time purchases, this field is ignored.
    #:
    #: For recurring payments, you should pass the expected average
    #: transaction amount (default 25.00). PayPal uses this value to validate
    #: the buyer’s funding source.
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
    #:     This field is required when implementing the Instant Update API
    #:     callback. PayPal recommends that the maximum total amount be
    #:     slightly greater than the sum of the line-item order details, tax,
    #:     and the shipping options of greatest value.
    maxamt = core.MoneyField()

    #: (Required) URL to which the buyer’s browser is returned after choosing
    #: to pay with PayPal. For digital goods, you must add JavaScript to this
    #: page to close the in-context experience.
    #:
    #:
    #: Character length and limitations:
    #:     2048 single-byte characters
    #:
    #:
    #: Notes:
    #:     PayPal recommends that the value be the final review page on which
    #:     the buyer confirms the order and payment or billing agreement.
    returnurl = core.URLField(required=True, max_length=2048)

    #: (Required) URL to which the buyer is returned if the buyer does not
    #: approve the use of PayPal to pay you. For digital goods, you must add
    #: JavaScript to this page to close the in-context experience.
    #:
    #:
    #: Character length and limitations:
    #:     2048 single-byte characters
    #:
    #:
    #: Notes:
    #:     PayPal recommends that the value be the original page on which the
    #:     buyer chose to pay with PayPal or establish a billing agreement.
    cancelurl = core.URLField(required=True, max_length=2048)

    #: (Optional) URL to which the callback request from PayPal is sent. It
    #: must start with HTTPS for production integration. It can start with
    #: HTTPS or HTTP for sandbox testing.
    #:
    #:
    #: Character length and limitations:
    #:     1024 single-byte characters
    #:
    #:
    #: Available since API version: 53.0
    callback = core.URLField(max_length=2048)

    #: (Optional) An override for you to request more or less time to be able
    #: to process the callback request and respond. The acceptable range for
    #: the override is ``1`` to ``6`` seconds. If you specify a value greater
    #: than ``6``, PayPal uses the default value of ``3`` seconds.
    #:
    #:
    #: Character length and limitations:
    #:     An integer between ``1`` and ``6``
    callbacktimeout = core.IntegerField(min=1, max=6)

    #: Indicates whether or not you require the buyer’s shipping address on
    #: file with PayPal be a confirmed address. For digital goods, this field
    #: is required, and you must set it to 0. It is one of the following
    #: values:
    #:
    #:     ``0`` – You do not require the buyer’s shipping address be a
    #:     confirmed address.
    #:
    #:     ``1 `` – You require the buyer’s shipping address be a confirmed
    #:     address.
    #:
    #:
    #: Character length and limitations:
    #:     1 single-byte numeric character
    #:
    #:
    #: Notes:
    #:     Setting this field overrides the setting you specified in your
    #:     Merchant Account Profile.
    reqconfirmshipping = core.BooleanField()

    #: Determines where or not PayPal displays shipping address fields on the
    #: PayPal pages. For digital goods, this field is required, and you must
    #: set it to 1. It is one of the following values:
    #:
    #:     ``0`` – PayPal displays the shipping address on the PayPal pages.
    #:
    #:     ``1`` – PayPal does not display shipping address
    #:     fields whatsoever.
    #:
    #:     ``2`` – If you do not pass the shipping address, PayPal obtains it
    #:     from the buyer’s account profile.
    #:
    #:
    #: Character length and limitations:
    #:     4 single-byte numeric characters
    noshipping = core.IntegerField(unsigned=True, max=2)

    #: (Optional) Enables the buyer to enter a note to the merchant on the
    #: PayPal page during checkout. The note is returned in the
    #: ``GetExpressCheckoutDetails`` response and the
    #: ``DoExpressCheckoutPayment`` response. It is one of the following
    #: values:
    #:
    #:     ``0`` – The buyer is unable to enter a note to the merchant.
    #:
    #:     ``1`` – The buyer is able to enter a note to the merchant.
    #:
    #:
    #: Character length and limitations:
    #:     1 single-byte numeric character
    #:
    #:
    #: Available since API version: 53.0
    allownote = core.BooleanField()

    #: (Optional) Determines whether or not the PayPal pages should display
    #: the shipping address set by you in this SetExpressCheckout request, not
    #: the shipping address on file with PayPal for this buyer. Displaying the
    #: PayPal street address on file does not allow the buyer to edit that
    #: address. It is one of the following values:
    #:
    #:     ``0`` – The PayPal pages should not display the shipping address.
    #:
    #:     ``1`` – The PayPal pages should display the shipping address.
    #:
    #:
    #: Character length and limitations:
    #:     1 single-byte numeric character
    addoverride = core.BooleanField()

    #: Version of the callback API. This field is required when implementing
    #: the Instant Update Callback API. It must be set to ``61.0`` or a later
    #: version.
    #:
    #:
    #: Available since API version: 61.0
    callbackversion = core.StringField()

    #: (Optional) Locale of pages displayed by PayPal during Express Checkout.
    #: It is one of the following country code values supported by PayPal
    #: (default is US):
    #:
    #:     ``AU`` – Australia
    #:
    #:     ``AT`` – Austria
    #:
    #:     ``BE`` – Belgium
    #:
    #:     ``BR`` – Brazil
    #:
    #:     ``CA`` – Canada
    #:
    #:     ``CH`` – Switzerland
    #:
    #:     ``CN`` – China
    #:
    #:     ``DE`` – Germany
    #:
    #:     ``ES`` – Spain
    #:
    #:     ``GB`` – United Kingdom
    #:
    #:     ``FR`` – France
    #:
    #:     ``IT`` – Italy
    #:
    #:     ``NL`` – Netherlands
    #:
    #:     ``PL`` – Poland
    #:
    #:     ``PT`` – Portugal
    #:
    #:     ``RU`` – Russia
    #:
    #:     ``US`` – United States
    #:
    #:     The following 5-character codes are also supported for languages in
    #:     specific countries:
    #:
    #:     ``da_DK`` – Danish (for Denmark only)
    #:
    #:     ``he_IL`` – Hebrew (all)
    #:
    #:     ``id_ID`` – Indonesian (for Indonesia only)
    #:
    #:     ``jp_JP`` – Japanese (for Japan only)
    #:
    #:     ``no_NO`` – Norwegian (for Norway only)
    #:
    #:     ``pt_BR`` – Brazilian Portuguese (for Portugal and Brazil only)
    #:
    #:     ``ru_RU`` – Russian (for Lithuania, Latvia, and Ukraine only)
    #:
    #:     ``sv_SE`` – Swedish (for Sweden only)
    #:
    #:     ``th_TH`` – Thai (for Thailand only)
    #:
    #:     ``tr_TR`` – Turkish (for Turkey only)
    #:
    #:     ``zh_CN`` – Simplified Chinese (for China only)
    #:
    #:     ``zh_HK`` – Traditional Chinese (for Hong Kong only)
    #:
    #:     ``zh_TW`` – Traditional Chinese (for Taiwan only)
    #:
    #:
    #: Character length and limitations:
    #:     2-character country code
    localecode = core.StringField(choices=countries.SUPPORTED_LOCALES)

    #: (Optional) Name of the Custom Payment Page Style for payment pages
    #: associated with this button or link. It corresponds to the HTML
    #: variable ``page_style`` for customizing payment pages. It is the same
    #: name as the Page Style Name you chose to add or edit the page style in
    #: your PayPal Account profile.
    #:
    #:
    #: Character length and limitations:
    #:     30 single-byte alphabetic characters
    pagestyle = core.StringField(max_length=30)

    #: (Optional) URL for the image you want to appear at the top left of the
    #: payment page. The image has a maximum size of 750 pixels wide by 90
    #: pixels high. PayPal recommends that you provide an image that is stored
    #: on a secure (https) server. If you do not specify an image, the
    #: business name displays.
    #:
    #:
    #: Character length and limitations:
    #:     127 single-byte alphanumeric characters
    hdrimg = core.URLField(max_length=127)

    #: (Optional) Sets the border color around the header of the payment page.
    #: The border is a 2-pixel perimeter around the header space, which is 750
    #: pixels wide by 90 pixels high. By default, the color is black.
    #:
    #:
    #: Character length and limitations:
    #:     6-character HTML hexadecimal ASCII color code
    hdrbordercolor = core.StringField(length=6)

    #: (Optional) Sets the background color for the header of the payment
    #: page. By default, the color is white.
    #:
    #:
    #: Character length and limitations:
    #:     6-character HTML hexadecimal ASCII color code
    hdrbackcolor = core.StringField(length=6)

    #: (Optional) Sets the background color for the payment page. By default,
    #: the color is white.
    #:
    #:
    #: Character length and limitations:
    #:     6-character HTML hexadecimal ASCII color code
    payflowcolor = core.StringField(length=6)

    #: (Optional) Email address of the buyer as entered during checkout.
    #: PayPal uses this value to pre-fill the PayPal membership sign-up
    #: portion on the PayPal pages.
    #:
    #:
    #: Character length and limitations:
    #:     127 single-byte alphanumeric characters
    email = core.StringField(length=127)

    #: (Optional) Type of checkout flow. It is one of the following values:
    #:
    #:     ``Sole`` – Buyer does not need to create a PayPal account to check
    #:     out. This is referred to as PayPal Account Optional.
    #:
    #:     ``Mark`` – Buyer must have a PayPal account to check out.
    #:
    #:
    #: Notes:
    #:     You can pass ``Mark`` to selectively override the PayPal Account
    #:     Optional setting if PayPal Account Optional is turned on in your
    #:     merchant account. Passing ``Sole`` has no effect if PayPal Account
    #:     Optional is turned off in your account
    solutiontype = core.StringField(choices=('Sole', 'Mark'))

    #: (Optional) Type of PayPal page to display. It is one of the following
    #: values:
    #:
    #:     ``Billing`` – Non-PayPal account
    #:
    #:     ``Login`` – PayPal account login
    landingpage = core.StringField(choices=('Billing', 'Login'))

    #: (Optional) Type of channel. It is one of the following values:
    #:
    #:     ``Merchant`` – Non-auction seller
    #:
    #:     ``eBayItem`` – eBay auction
    channeltype = core.StringField(choices=('Merchant', 'eBayItem'))

    #: (Optional) The URL on the merchant site to redirect to after a
    #: successful giropay payment.
    #:
    #:
    #: Notes:
    #:     Use this field only if you are using giropay or bank transfer
    #:     payment methods in Germany.
    giropaysuccessurl = core.URLField()

    #: (Optional) The URL on the merchant site to redirect to after a
    #: successful giropay payment.
    #:
    #:
    #: Notes:
    #:     Use this field only if you are using giropay or bank transfer
    #:     payment methods in Germany.
    giropaycancelurl = core.URLField()

    #: (Optional) The URL on the merchant site to transfer to after a bank
    #: transfer payment.
    #:
    #:
    #: Notes:
    #:     Use this field only if you are using giropay or bank transfer
    #:     payment methods in Germany.
    banktxnpendingurl = core.URLField()

    #: (Optional) A label that overrides the business name in the PayPal
    #: account on the PayPal hosted checkout pages.
    #:
    #:
    #: Character length and limitations:
    #:     127 single-byte alphanumeric characters
    brandname = core.StringField(max_length=127)

    #: (Optional) Merchant Customer Service number displayed on the PayPal
    #: pages.
    #:
    #:
    #: Character length and limitations:
    #:     16 single-byte characters
    customerservicenumber = core.StringField(max_length=16)

    #: (Optional) Enables the gift message widget on the PayPal pages. It is
    #: one of the following values:
    #:
    #:     ``0`` – Do not enable gift message widget.
    #:
    #:     ``1`` – Enable gift message widget.
    giftmessageenable = core.BooleanField()

    #: (Optional) Enable gift receipt widget on the PayPal pages. It is one of
    #: the following values:
    #:
    #:     ``0`` – Do not enable gift receipt widget.
    #:
    #:     ``1`` – Enable gift receipt widget.
    giftreceiptenable = core.BooleanField()

    #: (Optional) Enable gift wrap widget on the PayPal pages. It is one of
    #: the following values:
    #:
    #:     ``0`` – Do not enable gift wrap widget.
    #:
    #:     ``1 `` – Enable gift wrap widget.
    #:
    #:
    #: Notes:
    #:     If you pass the value ``1`` in this field, values for the gift wrap
    #:     amount and gift wrap name are not passed, the gift wrap name is not
    #:     displayed, and the gift wrap amount displays as 0.00.
    giftwrapenable = core.BooleanField()

    #: (Optional) Label for the gift wrap option such as “Box with ribbon.”
    #:
    #:
    #: Character length and limitations:
    #:     25 single-byte characters
    giftwrapname = core.StringField()

    #: (Optional) Amount to be charged to the buyer for gift wrapping..
    #:
    #:
    #: Character length and limitations:
    #:     Value is a positive number which cannot exceed $10,000 USD in any
    #:     currency. It includes no currency symbol. It must have 2 decimal
    #:     places, the decimal separator must be a period (.), and the
    #:     optional thousands separator must be a comma (,).
    giftwrapamount = core.MoneyField()

    #: (Optional) Enables the buyer to provide their email address on the
    #: PayPal pages to be notified of promotions or special events. Is one of
    #: the following values:
    #:
    #:     ``0`` – Do not enable buyer to provide email address.
    #:
    #:     ``1`` – Enable the buyer to provide email address.
    buyeremailoptinenable = core.BooleanField()

    #: (Optional) Text for the survey question on the PayPal pages. If the
    #: survey question is present, at least 2 survey answer options must be
    #: present.
    #:
    #:
    #: Character length and limitations:
    #:     50 single-byte characters
    surveyquestion = core.StringField(max_length=50)

    #: (Optional) Enables survey functionality. It is one of the following
    #: values:
    #:
    #:     ``0`` – Disables survey functionality.
    #:
    #:     ``1`` – Enables survey functionality.
    surveyenable = core.BooleanField()

    #: (Optional) Possible options for the survey answers on the PayPal pages.
    #: Answers are displayed only if a valid survey question is present.
    #:
    #:
    #: Character length and limitations:
    #:     15 single-byte characters
    surveychoice = core.ListStringField(
        validation_callback=core.gen_strlen_validator('surveychoice', 15),
    )

    #: List of ``PaymentRequestType`` instances
    paymentrequest = core.ListTypeField(instanceof=PaymentRequest,
                                        required=True)


class Response(core.Response):
    """SetExpressCheckout Response Type."""
    #: A timestamped token by which you identify to PayPal that you are
    #: processing this payment with Express Checkout. The token expires after
    #: three hours. If you set the token in the ``SetExpressCheckout``
    #: request, the value of the token in the response is identical to the
    #: value in the request.
    #:
    #:
    #: Character length and limitations:
    #:     20 single-byte characters
    token = core.StringField(max_length=20)

    def get_redirect_url(self, client):
        path = '/webscr?cmd=_express-checkout&token=%s' % self.token
        return client.generate_paypal_url(path)
