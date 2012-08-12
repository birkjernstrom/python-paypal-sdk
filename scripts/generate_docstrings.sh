#!/usr/bin/env bash
#
# Convert all PayPal API method documentations into docstrings
# intended to be used for the PayPal API types implemented in this
# Python implementation of the PayPal API suites.
#
# All API services will be contained within their own directory in the
# docstrings directory. Along with all their methods stored as separate
# files.
#
SCRIPT_PATH=$(readlink -f $0)
SCRIPT_DIR=$(dirname $SCRIPT_PATH)
DOCSTRINGS_DIR="${SCRIPT_DIR}/../docstrings"

PYTHON_PATH=$(which python)
GENERATOR_SCRIPT_NAME='scrape_method_documentation.py'

CACHE_DIR="${SCRIPT_DIR}/../cached_documentation"

function bail {
    printf "Incorrect usage of %s\n" $0
    exit 1
}

function mk_service_directory {
    if [ $# -lt 1 ]; then
        bail
    fi

    service_directory="${DOCSTRINGS_DIR}/${1}"
    if [[ ! -d $service_directory ]]; then
        printf "No directory corresponding to API service %s. Creating it.\n" $1
        mkdir -p $service_directory
    fi
}

function generate {
    if [ $# -lt 2 ]; then
        bail
    fi

    local API_SERVICE=$1
    local API_METHOD=$2

    mk_service_directory $API_SERVICE

    printf "===> Generate docstrings for %s.%s\n" $API_SERVICE $API_METHOD
    printf "Generating docstrings...\n"
    METHOD_FILENAME="${DOCSTRINGS_DIR}/${API_SERVICE}/${API_METHOD}.txt"
    $PYTHON_PATH $GENERATOR_SCRIPT_NAME $API_SERVICE $API_METHOD $CACHE_DIR > $METHOD_FILENAME
    if [ $? -eq 1 ]; then
        printf "Failed generating docstrings. Aborting!\n"
        exit 1
    fi
    printf "Done!\n"
}

###############################################################################
# ADAPTIVE ACCOUNTS
###############################################################################

generate AdaptiveAccounts AddBankAccount
generate AdaptiveAccounts AddPaymentCard
generate AdaptiveAccounts CreateAccount
generate AdaptiveAccounts GetUserAgreement
generate AdaptiveAccounts GetVerifiedStatus
generate AdaptiveAccounts SetFundingSourceConfirmed

###############################################################################
# ADAPTIVE PAYMENTS
###############################################################################

generate AdaptivePayments CancelPreapproval
generate AdaptivePayments ConvertCurrency
generate AdaptivePayments ExecutePayment
generate AdaptivePayments GetFundingPlans
generate AdaptivePayments GetPaymentOptions
generate AdaptivePayments GetShippingAddress
generate AdaptivePayments Pay
generate AdaptivePayments PaymentDetails
generate AdaptivePayments Preapproval
generate AdaptivePayments PreapprovalDetails
generate AdaptivePayments Refund
generate AdaptivePayments SetPaymentOptions

###############################################################################
# BUTTON MANAGER
###############################################################################

generate ButtonManager BMButtonSearch
generate ButtonManager BMGetButtonDetails
generate ButtonManager BMGetInventory
generate ButtonManager BMManageButtonStatus
generate ButtonManager BMSetInventory
generate ButtonManager BMUpdateButton

###############################################################################
# INVOICING
###############################################################################

generate Invoicing CancelInvoice
generate Invoicing CreateAndSendInvoice
generate Invoicing CreateInvoice
generate Invoicing GetInvoiceDetails
generate Invoicing MarkInvoiceAsPaid
generate Invoicing MarkInvoiceAsRefunded
generate Invoicing MarkInvoiceAsUnpaid
generate Invoicing SearchInvoices
generate Invoicing SendInvoice
generate Invoicing UpdateInvoice

###############################################################################
# EXPRESS CHECKOUT
###############################################################################

generate ExpressCheckout AddressVerify
generate ExpressCheckout BillOutstandingAmount
generate ExpressCheckout Callback
generate ExpressCheckout CreateRecurringPaymentsProfile
generate ExpressCheckout DoAuthorization
generate ExpressCheckout DoCapture
generate ExpressCheckout DoExpressCheckoutPayment
generate ExpressCheckout DoReauthorization
generate ExpressCheckout DoReferenceTransaction
generate ExpressCheckout DoVoid
generate ExpressCheckout GetBalance
generate ExpressCheckout GetBillingAgreementCustomerDetails
generate ExpressCheckout GetExpressCheckoutDetails
generate ExpressCheckout GetPalDetails
generate ExpressCheckout GetTransactionDetails
generate ExpressCheckout GetRecurringPaymentsProfileDetails
generate ExpressCheckout ManagePendingTransactionStatus
generate ExpressCheckout ManageRecurringPaymentsProfileStatus
generate ExpressCheckout RefundTransaction
generate ExpressCheckout SetCustomerBillingAgreement
generate ExpressCheckout SetExpressCheckout
generate ExpressCheckout TransactionSearch
generate ExpressCheckout UpdateRecurringPaymentsProfile

###############################################################################
# MASS PAY
###############################################################################

generate MassPay MassPay

###############################################################################
# PAYMENTS PRO
###############################################################################

generate PaymentsPro DoDirectPayment
generate PaymentsPro DoNonReferencedCredit

###############################################################################
# PERMISSIONS
###############################################################################

generate Permissions CancelPermissions
generate Permissions GetAccessToken
generate Permissions GetAdvancedPersonalData
generate Permissions GetBasicPersonalData
generate Permissions GetPermissions
generate Permissions RequestPermissions
