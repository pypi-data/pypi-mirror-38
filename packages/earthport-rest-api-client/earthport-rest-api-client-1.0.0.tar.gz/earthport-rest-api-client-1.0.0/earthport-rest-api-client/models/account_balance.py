# -*- coding: utf-8 -*-

import earthport-rest-api-client.models.monetary_value

class AccountBalance(object):

    """Implementation of the 'AccountBalance' model.

    This element represents the balance of a merchant account or a managed
    merchant account.

    Attributes:
        balance (MonetaryValue): Represents a monetary value containing a
            decimal amount value along with a currency code. The currency code
            is a three letter ISO 4217 code. E.g. GBP for British sterling
            pounds.
        balance_timestamp (string): TODO: type description here.
        last_movement_timestamp (string): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "balance":'balance',
        "balance_timestamp":'balanceTimestamp',
        "last_movement_timestamp":'lastMovementTimestamp'
    }

    def __init__(self,
                 balance=None,
                 balance_timestamp=None,
                 last_movement_timestamp=None):
        """Constructor for the AccountBalance class"""

        # Initialize members of the class
        self.balance = balance
        self.balance_timestamp = balance_timestamp
        self.last_movement_timestamp = last_movement_timestamp


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
        balance = earthport-rest-api-client.models.monetary_value.MonetaryValue.from_dictionary(dictionary.get('balance')) if dictionary.get('balance') else None
        balance_timestamp = dictionary.get('balanceTimestamp')
        last_movement_timestamp = dictionary.get('lastMovementTimestamp')

        # Return an object of this model
        return cls(balance,
                   balance_timestamp,
                   last_movement_timestamp)


