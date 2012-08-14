# -*- coding: utf-8 -*-

__all__ = [
    # Modules
    'types', 'client', 'exceptions',

    # Client aliases
    'Client',

    # Exception aliases
    'InvalidRequestException', 'InvalidResponseException',
]

from paypal import types, client, exceptions

###############################################################################
# ALIASES
###############################################################################

#----------------------------------------
# Client Aliases
#----------------------------------------

#: Alias for ``client.Client``
Client = client.Client
#: Alias for ``client.Config``
Config = client.Config

#----------------------------------------
# Exception Aliases
#----------------------------------------

#: Alias for ``exceptions.InvalidRequestException``
InvalidRequestException = exceptions.InvalidRequestException
#: Alias for ``exceptions.InvalidResponseException``
InvalidResponseException = exceptions.InvalidResponseException
