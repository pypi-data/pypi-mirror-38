# -*- coding: utf-8 -*-

import earthport-rest-api-client.models.transaction_id
import earthport-rest-api-client.models.financial_transaction_status
import earthport-rest-api-client.models.monetary_value
import earthport-rest-api-client.models.statement_detail
import earthport-rest-api-client.models.users_bank_id

class PayoutTransactionShort(object):

    """Implementation of the 'PayoutTransactionShort' model.

    A financial transaction representing a payout from an account held in the
    EPS system.

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
        users_bank_id (UsersBankID): This group consists of a collection of
            both the user ID group and beneficiary bank ID group. The 'userID'
            is a collection of user identifier types. The 'benBankID' is a
            collection of account identifier types. Both the 'userID' and
            'benBankID' fields are mandatory.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "transaction_id":'transactionID',
        "timestamp":'timestamp',
        "transaction_type":'transactionType',
        "amount":'amount',
        "movement_type":'movementType',
        "users_bank_id":'usersBankId',
        "transaction_status":'transactionStatus',
        "statement_details":'statementDetails'
    }

    def __init__(self,
                 transaction_id=None,
                 timestamp=None,
                 transaction_type=None,
                 amount=None,
                 movement_type=None,
                 users_bank_id=None,
                 transaction_status=None,
                 statement_details=None):
        """Constructor for the PayoutTransactionShort class"""

        # Initialize members of the class
        self.transaction_id = transaction_id
        self.timestamp = timestamp
        self.transaction_type = transaction_type
        self.transaction_status = transaction_status
        self.amount = amount
        self.movement_type = movement_type
        self.statement_details = statement_details
        self.users_bank_id = users_bank_id


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
        users_bank_id = earthport-rest-api-client.models.users_bank_id.UsersBankID.from_dictionary(dictionary.get('usersBankId')) if dictionary.get('usersBankId') else None
        transaction_status = earthport-rest-api-client.models.financial_transaction_status.FinancialTransactionStatus.from_dictionary(dictionary.get('transactionStatus')) if dictionary.get('transactionStatus') else None
        statement_details = None
        if dictionary.get('statementDetails') != None:
            statement_details = list()
            for structure in dictionary.get('statementDetails'):
                statement_details.append(earthport-rest-api-client.models.statement_detail.StatementDetail.from_dictionary(structure))

        # Return an object of this model
        return cls(transaction_id,
                   timestamp,
                   transaction_type,
                   amount,
                   movement_type,
                   users_bank_id,
                   transaction_status,
                   statement_details)


