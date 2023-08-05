# -*- coding: utf-8 -*-

import earthport-rest-api-client.models.financial_transaction
import earthport-rest-api-client.models.pagination_result

class SearchTransactionsResponse(object):

    """Implementation of the 'Search TransactionsResponse' model.

    Transactions.

    Attributes:
        transactions (list of FinancialTransaction): TODO: type description
            here.
        pagination_result (PaginationResult): This returns a paged set of
            results rather than the full result set.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "transactions":'transactions',
        "pagination_result":'paginationResult'
    }

    def __init__(self,
                 transactions=None,
                 pagination_result=None):
        """Constructor for the SearchTransactionsResponse class"""

        # Initialize members of the class
        self.transactions = transactions
        self.pagination_result = pagination_result


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
        transactions = None
        if dictionary.get('transactions') != None:
            transactions = list()
            for structure in dictionary.get('transactions'):
                transactions.append(earthport-rest-api-client.models.financial_transaction.FinancialTransaction.from_dictionary(structure))
        pagination_result = earthport-rest-api-client.models.pagination_result.PaginationResult.from_dictionary(dictionary.get('paginationResult')) if dictionary.get('paginationResult') else None

        # Return an object of this model
        return cls(transactions,
                   pagination_result)


