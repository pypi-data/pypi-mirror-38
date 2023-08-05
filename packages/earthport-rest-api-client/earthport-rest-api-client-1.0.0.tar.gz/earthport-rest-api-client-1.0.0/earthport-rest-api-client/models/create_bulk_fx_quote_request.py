# -*- coding: utf-8 -*-


class CreateBulkFXQuoteRequest(object):

    """Implementation of the 'CreateBulkFXQuoteRequest' model.

    Quote Request.

    Attributes:
        sell_currency (string): Valid supported ISO 4217 3-character currency
            code.
        buy_currency (string): Valid supported ISO 4217 3-character currency
            code.
        buy_country (string): Valid supported ISO 3166 2-character country
            code.
        service_level (ServiceLevelEnum): Supported service levels for a
            payout request (standard or express).

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "sell_currency":'sellCurrency',
        "buy_currency":'buyCurrency',
        "buy_country":'buyCountry',
        "service_level":'serviceLevel'
    }

    def __init__(self,
                 sell_currency=None,
                 buy_currency=None,
                 buy_country=None,
                 service_level=None):
        """Constructor for the CreateBulkFXQuoteRequest class"""

        # Initialize members of the class
        self.sell_currency = sell_currency
        self.buy_currency = buy_currency
        self.buy_country = buy_country
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
        sell_currency = dictionary.get('sellCurrency')
        buy_currency = dictionary.get('buyCurrency')
        buy_country = dictionary.get('buyCountry')
        service_level = dictionary.get('serviceLevel')

        # Return an object of this model
        return cls(sell_currency,
                   buy_currency,
                   buy_country,
                   service_level)


