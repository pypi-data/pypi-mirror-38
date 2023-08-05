# -*- coding: utf-8 -*-

import earthport-rest-api-client.models.statement_line_item
import earthport-rest-api-client.models.account_balance
import earthport-rest-api-client.models.pagination_result

class Statement(object):

    """Implementation of the 'Statement' model.

    TODO: type model description here.

    Attributes:
        statement_line_items (list of StatementLineItem): TODO: type
            description here.
        opening_balance (AccountBalance): This element represents the balance
            of a merchant account or a managed merchant account.
        closing_balance (AccountBalance): This element represents the balance
            of a merchant account or a managed merchant account.
        pagination_result (PaginationResult): This returns a paged set of
            results rather than the full result set.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "statement_line_items":'statementLineItems',
        "opening_balance":'openingBalance',
        "closing_balance":'closingBalance',
        "pagination_result":'paginationResult'
    }

    def __init__(self,
                 statement_line_items=None,
                 opening_balance=None,
                 closing_balance=None,
                 pagination_result=None):
        """Constructor for the Statement class"""

        # Initialize members of the class
        self.statement_line_items = statement_line_items
        self.opening_balance = opening_balance
        self.closing_balance = closing_balance
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
        statement_line_items = None
        if dictionary.get('statementLineItems') != None:
            statement_line_items = list()
            for structure in dictionary.get('statementLineItems'):
                statement_line_items.append(earthport-rest-api-client.models.statement_line_item.StatementLineItem.from_dictionary(structure))
        opening_balance = earthport-rest-api-client.models.account_balance.AccountBalance.from_dictionary(dictionary.get('openingBalance')) if dictionary.get('openingBalance') else None
        closing_balance = earthport-rest-api-client.models.account_balance.AccountBalance.from_dictionary(dictionary.get('closingBalance')) if dictionary.get('closingBalance') else None
        pagination_result = earthport-rest-api-client.models.pagination_result.PaginationResult.from_dictionary(dictionary.get('paginationResult')) if dictionary.get('paginationResult') else None

        # Return an object of this model
        return cls(statement_line_items,
                   opening_balance,
                   closing_balance,
                   pagination_result)


