# -*- coding: utf-8 -*-

import earthport-rest-api-client.models.monetary_value
import earthport-rest-api-client.models.fx_rate

class FXDetail(object):

    """Implementation of the 'FXDetail' model.

    Represents the details of an FX transaction, encapsulating the sellAmount,
    buyAmount and fxRate into a single type.

    Attributes:
        buy_amount (MonetaryValue): Represents a monetary value containing a
            decimal amount value along with a currency code. The currency code
            is a three letter ISO 4217 code. E.g. GBP for British sterling
            pounds.
        fx_rate (FXRate): Represents an FX rate between two currencies, the
            rate is restricted to 6 decimal places. The currency code is a
            three letter ISO 4217 code. E.g. GBP for British sterling pounds.
        sell_amount (MonetaryValue): Represents a monetary value containing a
            decimal amount value along with a currency code. The currency code
            is a three letter ISO 4217 code. E.g. GBP for British sterling
            pounds.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "buy_amount":'buyAmount',
        "fx_rate":'fxRate',
        "sell_amount":'sellAmount'
    }

    def __init__(self,
                 buy_amount=None,
                 fx_rate=None,
                 sell_amount=None):
        """Constructor for the FXDetail class"""

        # Initialize members of the class
        self.buy_amount = buy_amount
        self.fx_rate = fx_rate
        self.sell_amount = sell_amount


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
        buy_amount = earthport-rest-api-client.models.monetary_value.MonetaryValue.from_dictionary(dictionary.get('buyAmount')) if dictionary.get('buyAmount') else None
        fx_rate = earthport-rest-api-client.models.fx_rate.FXRate.from_dictionary(dictionary.get('fxRate')) if dictionary.get('fxRate') else None
        sell_amount = earthport-rest-api-client.models.monetary_value.MonetaryValue.from_dictionary(dictionary.get('sellAmount')) if dictionary.get('sellAmount') else None

        # Return an object of this model
        return cls(buy_amount,
                   fx_rate,
                   sell_amount)


