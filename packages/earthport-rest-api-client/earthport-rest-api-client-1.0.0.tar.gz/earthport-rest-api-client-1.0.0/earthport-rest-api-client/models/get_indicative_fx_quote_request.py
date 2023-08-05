# -*- coding: utf-8 -*-

import earthport-rest-api-client.models.monetary_value

class GetIndicativeFXQuoteRequest(object):

    """Implementation of the 'GetIndicativeFXQuoteRequest' model.

    TODO: type model description here.

    Attributes:
        sell_amount (MonetaryValue): Represents a monetary value containing a
            decimal amount value along with a currency code. The currency code
            is a three letter ISO 4217 code. E.g. GBP for British sterling
            pounds.
        buy_currency (string): Valid supported ISO 4217 3-character currency
            code.
        buy_amount (MonetaryValue): Represents a monetary value containing a
            decimal amount value along with a currency code. The currency code
            is a three letter ISO 4217 code. E.g. GBP for British sterling
            pounds.
        sell_currency (string): Valid supported ISO 4217 3-character currency
            code.
        service_level (ServiceLevelEnum): Supported service levels for a
            payout request (standard or express).

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "sell_amount":'sellAmount',
        "buy_currency":'buyCurrency',
        "buy_amount":'buyAmount',
        "sell_currency":'sellCurrency',
        "service_level":'serviceLevel'
    }

    def __init__(self,
                 sell_amount=None,
                 buy_currency=None,
                 buy_amount=None,
                 sell_currency=None,
                 service_level=None):
        """Constructor for the GetIndicativeFXQuoteRequest class"""

        # Initialize members of the class
        self.sell_amount = sell_amount
        self.buy_currency = buy_currency
        self.buy_amount = buy_amount
        self.sell_currency = sell_currency
        self.service_level = service_level


    @classmethod
    def from_dictionary(cls,
                        dictionary):
        """Creates an instance of this model from a dictionary

        Args:
            dictionary (dictionary): A dictionary representation of the object as
            obtained from the deserialization of the server's response. The keys
            MUST match property names in the API description.

        Returns:
            object: An instance of this structure class.

        """
        if dictionary is None:
            return None

        # Extract variables from the dictionary
        sell_amount = earthport-rest-api-client.models.monetary_value.MonetaryValue.from_dictionary(dictionary.get('sellAmount')) if dictionary.get('sellAmount') else None
        buy_currency = dictionary.get('buyCurrency')
        buy_amount = earthport-rest-api-client.models.monetary_value.MonetaryValue.from_dictionary(dictionary.get('buyAmount')) if dictionary.get('buyAmount') else None
        sell_currency = dictionary.get('sellCurrency')
        service_level = dictionary.get('serviceLevel')

        # Return an object of this model
        return cls(sell_amount,
                   buy_currency,
                   buy_amount,
                   sell_currency,
                   service_level)


