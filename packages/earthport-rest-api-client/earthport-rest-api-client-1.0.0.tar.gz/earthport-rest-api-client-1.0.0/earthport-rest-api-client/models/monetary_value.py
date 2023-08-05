# -*- coding: utf-8 -*-


class MonetaryValue(object):

    """Implementation of the 'MonetaryValue' model.

    Represents a monetary value containing a decimal amount value along with a
    currency code. The currency code is a three letter ISO 4217 code. E.g. GBP
    for British sterling pounds.

    Attributes:
        amount (float): TODO: type description here.
        currency (string): Valid supported ISO 4217 3-character currency
            code.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "amount":'amount',
        "currency":'currency'
    }

    def __init__(self,
                 amount=None,
                 currency=None):
        """Constructor for the MonetaryValue class"""

        # Initialize members of the class
        self.amount = amount
        self.currency = currency


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
        amount = dictionary.get('amount')
        currency = dictionary.get('currency')

        # Return an object of this model
        return cls(amount,
                   currency)


