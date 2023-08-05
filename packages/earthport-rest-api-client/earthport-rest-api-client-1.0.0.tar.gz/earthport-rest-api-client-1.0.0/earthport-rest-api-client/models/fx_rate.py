# -*- coding: utf-8 -*-


class FXRate(object):

    """Implementation of the 'FXRate' model.

    Represents an FX rate between two currencies, the rate is restricted to 6
    decimal places. The currency code is a three letter ISO 4217 code. E.g.
    GBP for British sterling pounds.

    Attributes:
        buy_currency (string): Valid supported ISO 4217 3-character currency
            code.
        rate (float): TODO: type description here.
        sell_currency (string): Valid supported ISO 4217 3-character currency
            code.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "buy_currency":'buyCurrency',
        "rate":'rate',
        "sell_currency":'sellCurrency'
    }

    def __init__(self,
                 buy_currency=None,
                 rate=None,
                 sell_currency=None):
        """Constructor for the FXRate class"""

        # Initialize members of the class
        self.buy_currency = buy_currency
        self.rate = rate
        self.sell_currency = sell_currency


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
        buy_currency = dictionary.get('buyCurrency')
        rate = dictionary.get('rate')
        sell_currency = dictionary.get('sellCurrency')

        # Return an object of this model
        return cls(buy_currency,
                   rate,
                   sell_currency)


