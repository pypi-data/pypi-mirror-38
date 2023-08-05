# -*- coding: utf-8 -*-


class BulkFXDetail(object):

    """Implementation of the 'BulkFXDetail' model.

    TODO: type model description here.

    Attributes:
        sell_currency (string): Valid supported ISO 4217 3-character currency
            code.
        buy_currency (string): Valid supported ISO 4217 3-character currency
            code.
        buy_country (string): Valid supported ISO 3166 2-character country
            code.
        service_level (ServiceLevelEnum): Supported service levels for a
            payout request (standard or express).
        buy_fx_rate (float): TODO: type description here.
        sell_fx_rate (float): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "sell_currency":'sellCurrency',
        "buy_currency":'buyCurrency',
        "buy_country":'buyCountry',
        "service_level":'serviceLevel',
        "buy_fx_rate":'buyFxRate',
        "sell_fx_rate":'sellFxRate'
    }

    def __init__(self,
                 sell_currency=None,
                 buy_currency=None,
                 buy_country=None,
                 service_level=None,
                 buy_fx_rate=None,
                 sell_fx_rate=None):
        """Constructor for the BulkFXDetail class"""

        # Initialize members of the class
        self.sell_currency = sell_currency
        self.buy_currency = buy_currency
        self.buy_country = buy_country
        self.service_level = service_level
        self.buy_fx_rate = buy_fx_rate
        self.sell_fx_rate = sell_fx_rate


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
        sell_currency = dictionary.get('sellCurrency')
        buy_currency = dictionary.get('buyCurrency')
        buy_country = dictionary.get('buyCountry')
        service_level = dictionary.get('serviceLevel')
        buy_fx_rate = dictionary.get('buyFxRate')
        sell_fx_rate = dictionary.get('sellFxRate')

        # Return an object of this model
        return cls(sell_currency,
                   buy_currency,
                   buy_country,
                   service_level,
                   buy_fx_rate,
                   sell_fx_rate)


