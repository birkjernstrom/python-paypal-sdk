# -*- coding: utf-8 -*-
import re
from urlparse import parse_qsl

from paypal.util import ipn_logger


def log(notification, method, message, *args):
    prepend = 'IPN'
    txn_id = notification.txn_id
    if txn_id:
        prepend = '%s [TID: %s' % (prepend, txn_id)
        parent_txn_id = notification.get('parent_txn_id', None)
        if parent_txn_id:
            prepend = '%s PTID: %s' % (prepend, parent_txn_id)
        prepend += ']'

    # Make sure the notification does not contain any values that could affect
    # log formatting, like percentages.
    for key, value in notification.iteritems():
        if isinstance(value, basestring):
            notification[key] = re.sub('%', '', value)

    message = '%s: %s' % (prepend, message)
    message = message.format(notification=notification)
    write = getattr(ipn_logger, method)
    write(message, *args)


class Notification(dict):
    @staticmethod
    def decode(encoded_notification):
        # Although certain Instant Payment Notification payloads appear
        # to adhere to the NVP format they are not to be considered as such.
        # For instance list values are no represented accurately since the
        # key will begin at index 0 causing an IndexError exception to be
        # raised in the NVP module. Along with breaking hierarchical
        # structures by assigning string values for both address_country and
        # address_country_code. Causing TypeError exceptions to be raised.
        #
        # Another important thing to note here is that we convert the
        # query string pairs into a dictionary. Which could cause key
        # collision in case multiple values where to be given for the same
        # paramter. However, PayPal never does this in IPN notifications
        # which is why this technique is considered safe.
        params = dict(parse_qsl(encoded_notification))
        charset = params.get('charset', 'utf-8')

        def d(value):
            if isinstance(value, bytes):
                return value.decode(charset)
            return value
        return dict((d(k), d(v)) for k, v in params.iteritems())

    @classmethod
    def get_decoded_instance(cls, encoded_notification):
        return cls(cls.decode(encoded_notification))

    def get_transaction_type(self):
        return self.get('txn_type', None)

    transaction_type = property(get_transaction_type)

    def get_status_key(self):
        payment_status = self.get('payment_status', '').lower()
        if not payment_status:
            return None

    status_key = property(get_status_key)

    def is_sandbox(self):
        return self.test_ipn == '1'

    def __getattr__(self, name):
        """Allow retrieval of notification dict as though they
        where object properties. For example:

            >>> from paypal.ipn import Notification
            >>> n = Notification(txn_type='cart')
            >>> n.txn_type
            'cart'
            >>> n['txn_type']
            'cart'
        """
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)


class Listener(object):
    VERIFICATION_PATH = '/cgi-bin/webscr?cmd=_notify-validate'

    def __init__(self, client):
        self._client = client
        self.callbacks = {}
        self.default_callback = self.default_notification_handler

    client = property(lambda self: self._client)

    def add_callback(self, transaction_type, callback):
        callbacks = self.callbacks.setdefault(transaction_type, [])
        callbacks.append(callback)

    def default_notification_handler(self, notification):
        log(notification, 'error', (
            'Could not dispatch given notification since either no callbacks '
            'where assigned to the transaction type or a transaction type '
            'is not specified in the notification: {notification}'
        ))

    def dispatch(self, encoded_notification):
        try:
            # Ensure we log the notification even in the unlikely event of
            # catching an exception during the decoding procedure.
            get_decoded = Notification.get_decoded_instance
            notification = get_decoded(encoded_notification)
        except Exception:
            message = 'IPN: Cannot decode given notification: %s'
            ipn_logger.critical(message, encoded_notification)
            return False

        message = 'Received notification: {notification}'
        log(notification, 'info', message)
        if not self.send_verification(encoded_notification, notification):
            return False

        transaction_type = notification.get_transaction_type()
        if not transaction_type:
            self.default_callback(notification)
            return False

        callbacks = self.callbacks.get(transaction_type, None)
        if not callbacks:
            self.default_callback(notification)
            return False

        for callback in callbacks:
            log(notification, 'debug', 'Executing callback: %s', callback)
            callback(notification)

    def get_verification_url(self):
        url = getattr(self, '_verification_url', None)
        if url is not None:
            return url

        url = self.client.generate_paypal_url(self.VERIFICATION_PATH)
        self._verification_url = url
        return url

    def send_verification(self, encoded_notification, notification):
        def logger(message):
            message = 'Could not verify notification due to %s' % message
            log(notification, 'error', message)

        response, code = self.client.execute_request(
            self.get_verification_url(),
            encoded_notification,
            logger=logger,
        )

        if response is None:
            # Logging is not required since it is handled in the
            # execution of the verification request.
            return False

        if code != 200:
            message = 'Could not verify notification due to HTTP code %s'
            log(notification, 'error', message, code)
            return False

        if response == 'VERIFIED':
            log(notification, 'info', 'Notification verified by PayPal')
            return True

        log(
            notification, 'error',
            'Could not verify notification! Received inaccurate '
            'response which does not contain the string "VERIFIED": %s',
            response,
        )
        return False
