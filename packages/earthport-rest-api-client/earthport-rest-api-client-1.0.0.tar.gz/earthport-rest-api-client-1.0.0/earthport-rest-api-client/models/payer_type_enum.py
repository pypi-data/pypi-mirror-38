# -*- coding: utf-8 -*-

class PayerTypeEnum(object):

    """Implementation of the 'PayerType' enum.

    The type of Payer making the payment. This detrmines which identity
    details are used as the payer identity.

    Attributes:
        AUTHENTICATEDCALLER: Payout is being requested on behalf of the
            requesting merchant.
        MANAGEDMERCHANT: Payout is being requested on behalf of a managed
            merchant.
        USER: Payout is being requested on behalf of a user.

    """

    AUTHENTICATEDCALLER = 'authenticatedCaller'

    MANAGEDMERCHANT = 'managedMerchant'

    USER = 'user'

