# -*- coding: utf-8 -*-

import earthport-rest-api-client.models.transaction_id
import earthport-rest-api-client.models.financial_transaction_status
import earthport-rest-api-client.models.monetary_value
import earthport-rest-api-client.models.statement_detail

class GenericTransaction(object):

    """Implementation of the 'GenericTransaction' model.

    A generic financial transaction used to represent different types of
    transactions in the EPS system that do not have their own specific
    mappings in the schema.

    Attributes:
        transaction_id (TransactionID): Transaction ID type which contains
            both the unique Earthport transaction ID and the merchant supplied
            transaction ID.
        timestamp (string): TODO: type description here.
        transaction_type (string): TODO: type description here.
        transaction_status (FinancialTransactionStatus): Additional important
            status information for specific transaction types.
        amount (MonetaryValue): Represents a monetary value containing a
            decimal amount value along with a currency code. The currency code
            is a three letter ISO 4217 code. E.g. GBP for British sterling
            pounds.
        movement_type (MoneyMovementTypeEnum): Specifies whether a money
            movement is a debit or credit
        statement_details (list of StatementDetail): TODO: type description
            here.
        description (string): Any additional information about the
            transaction.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "transaction_id":'transactionID',
        "timestamp":'timestamp',
        "transaction_type":'transactionType',
        "amount":'amount',
        "movement_type":'movementType',
        "transaction_status":'transactionStatus',
        "statement_details":'statementDetails',
        "description":'description'
    }

    def __init__(self,
                 transaction_id=None,
                 timestamp=None,
                 transaction_type=None,
                 amount=None,
                 movement_type=None,
                 transaction_status=None,
                 statement_details=None,
                 description=None):
        """Constructor for the GenericTransaction class"""

        # Initialize members of the class
        self.transaction_id = transaction_id
        self.timestamp = timestamp
        self.transaction_type = transaction_type
        self.transaction_status = transaction_status
        self.amount = amount
        self.movement_type = movement_type
        self.statement_details = statement_details
        self.description = description


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
        transaction_id = earthport-rest-api-client.models.transaction_id.TransactionID.from_dictionary(dictionary.get('transactionID')) if dictionary.get('transactionID') else None
        timestamp = dictionary.get('timestamp')
        transaction_type = dictionary.get('transactionType')
        amount = earthport-rest-api-client.models.monetary_value.MonetaryValue.from_dictionary(dictionary.get('amount')) if dictionary.get('amount') else None
        movement_type = dictionary.get('movementType')
        transaction_status = earthport-rest-api-client.models.financial_transaction_status.FinancialTransactionStatus.from_dictionary(dictionary.get('transactionStatus')) if dictionary.get('transactionStatus') else None
        statement_details = None
        if dictionary.get('statementDetails') != None:
            statement_details = list()
            for structure in dictionary.get('statementDetails'):
                statement_details.append(earthport-rest-api-client.models.statement_detail.StatementDetail.from_dictionary(structure))
        description = dictionary.get('description')

        # Return an object of this model
        return cls(transaction_id,
                   timestamp,
                   transaction_type,
                   amount,
                   movement_type,
                   transaction_status,
                   statement_details,
                   description)


