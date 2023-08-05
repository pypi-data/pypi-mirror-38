# -*- coding: utf-8 -*-

class TransactionTypeEnum(object):

    """Implementation of the 'transactionType' enum.

    TODO: type enum description here.

    Attributes:
        PAYOUT: TODO: type description here.
        REFUND: TODO: type description here.
        ENUM_USER DEPOSIT: TODO: type description here.
        ENUM_MERCHANT LIQUIDITY DEPOSIT: TODO: type description here.
        ENUM_EARTHPORT TO MERCHANT LIQUIDITY TRANSFER: TODO: type description
            here.
        ENUM_MERCHANT LIQUIDITY MOVEMENT: TODO: type description here.
        JOURNAL: TODO: type description here.
        ENUM_GENERIC TRANSACTION: TODO: type description here.

    """

    PAYOUT = 'Payout'

    REFUND = 'Refund'

    ENUM_USER_DEPOSIT = 'User Deposit'

    ENUM_MERCHANT_LIQUIDITY_DEPOSIT = 'Merchant Liquidity Deposit'

    ENUM_EARTHPORT_TO_MERCHANT_LIQUIDITY_TRANSFER = 'Earthport to Merchant Liquidity Transfer'

    ENUM_MERCHANT_LIQUIDITY_MOVEMENT = 'Merchant Liquidity Movement'

    JOURNAL = 'Journal'

    ENUM_GENERIC_TRANSACTION = 'Generic Transaction'

