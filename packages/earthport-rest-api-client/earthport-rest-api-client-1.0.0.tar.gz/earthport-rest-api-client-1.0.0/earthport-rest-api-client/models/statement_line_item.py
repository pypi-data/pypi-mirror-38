# -*- coding: utf-8 -*-

import earthport-rest-api-client.models.financial_transaction

class StatementLineItem(object):

    """Implementation of the 'StatementLineItem' model.

    A statement line item is a financial transaction that affects the balance
    of an account.

    Attributes:
        transaction (FinancialTransaction): Minimum set of data that
            constitutes a financial transaction.
        balance (float): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "transaction":'transaction',
        "balance":'balance'
    }

    def __init__(self,
                 transaction=None,
                 balance=None):
        """Constructor for the StatementLineItem class"""

        # Initialize members of the class
        self.transaction = transaction
        self.balance = balance


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
        transaction = earthport-rest-api-client.models.financial_transaction.FinancialTransaction.from_dictionary(dictionary.get('transaction')) if dictionary.get('transaction') else None
        balance = dictionary.get('balance')

        # Return an object of this model
        return cls(transaction,
                   balance)


