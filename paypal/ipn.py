# -*- coding: utf-8 -*-
"""
"""

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

    message = message.format(notification)
    message = '%s: %s' % (prepend, message)
    write = getattr(ipn_logger, method)
    write(message, *args)


class Notification(dict):
    @staticmethod
    def decode(encoded_notification):
        return dict(parse_qsl(encoded_notification))

    @classmethod
    def get_decoded_instance(cls, encoded_notification):
        return cls(cls.decode(encoded_notification))

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

    client = property(lambda self: self._client)

    def add_callback(self, transaction_type, callback):
        callbacks = self.callbacks.setdefault(transaction_type, [])
        callbacks.append(callback)

    def dispatch(self, encoded_notification):
        notification = Notification.get_decoded_instance(encoded_notification)
        log(notification, 'info', 'Received notification: %s => {0}')
        if not self.send_verification(encoded_notification, notification):
            return False

        transaction_type = notification.txn_type
        if not transaction_type:
            message = 'Ignoring notification due to missing transaction type!'
            log(notification, 'error', message)
            return False

        callbacks = self.callbacks.get(transaction_type, None)
        if not callbacks:
            message = 'No callbacks registered to IPN transactions of type: %s'
            log(notification, 'warn', message, transaction_type)
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

        response = self.client.execute_request(
            self.get_verification_url(),
            encoded_notification,
            logger=logger,
        )

        if response is None:
            # Logging is not required since it is handled in the
            # execution of the verification request.
            return False

        http_code = response.getcode()
        if http_code != 200:
            message = 'Could not verify notification due to HTTP code %s'
            log(notification, 'error', message, http_code)
            return False

        response_body = response.read()
        if response_body == 'VERIFIED':
            return True

        log(
            notification, 'error',
            'Could not verify notification! Received inaccurate '
            'response which does not contain the string "VERIFIED": %s',
            response_body,
        )
        return False
