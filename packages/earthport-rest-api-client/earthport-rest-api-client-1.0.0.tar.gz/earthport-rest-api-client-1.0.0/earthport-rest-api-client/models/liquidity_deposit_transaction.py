# -*- coding: utf-8 -*-

import earthport-rest-api-client.models.transaction_id
import earthport-rest-api-client.models.financial_transaction_status
import earthport-rest-api-client.models.monetary_value
import earthport-rest-api-client.models.statement_detail
import earthport-rest-api-client.models.fx_executed_rate

class LiquidityDepositTransaction(object):

    """Implementation of the 'LiquidityDepositTransaction' model.

    Financial transaction representing a deposit of liquidity (money) into a
    merchant account.

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
        amount_credited_to_merchant_account (MonetaryValue): Represents a
            monetary value containing a decimal amount value along with a
            currency code. The currency code is a three letter ISO 4217 code.
            E.g. GBP for British sterling pounds.
        amount_recieved_at_bank (MonetaryValue): Represents a monetary value
            containing a decimal amount value along with a currency code. The
            currency code is a three letter ISO 4217 code. E.g. GBP for
            British sterling pounds.
        deposit_country (string): Valid supported ISO 3166 2-character country
            code.
        deposit_date (string): Valid ISO 8601 date format YYYY-MM-DD.
        deposit_reference (string): A Merchant User Deposit Reference.
        fx_executed_detail (FXExecutedRate): Holds details of an executed FX
            conversion that has occured as part of a financial transaction.
            The FX that occured was from the sellCurrency to the buyCurrency
            at a particular rate. The rate may have been requested via an FX
            Quote (fxTicketID). An FX conversion fee may have been applied to
            certain transaction types.
        unapplied_reason (string): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "transaction_id":'transactionID',
        "timestamp":'timestamp',
        "transaction_type":'transactionType',
        "amount":'amount',
        "movement_type":'movementType',
        "amount_credited_to_merchant_account":'amountCreditedToMerchantAccount',
        "amount_recieved_at_bank":'amountRecievedAtBank',
        "deposit_country":'depositCountry',
        "deposit_date":'depositDate',
        "transaction_status":'transactionStatus',
        "statement_details":'statementDetails',
        "deposit_reference":'depositReference',
        "fx_executed_detail":'fxExecutedDetail',
        "unapplied_reason":'unappliedReason'
    }

    def __init__(self,
                 transaction_id=None,
                 timestamp=None,
                 transaction_type=None,
                 amount=None,
                 movement_type=None,
                 amount_credited_to_merchant_account=None,
                 amount_recieved_at_bank=None,
                 deposit_country=None,
                 deposit_date=None,
                 transaction_status=None,
                 statement_details=None,
                 deposit_reference=None,
                 fx_executed_detail=None,
                 unapplied_reason=None):
        """Constructor for the LiquidityDepositTransaction class"""

        # Initialize members of the class
        self.transaction_id = transaction_id
        self.timestamp = timestamp
        self.transaction_type = transaction_type
        self.transaction_status = transaction_status
        self.amount = amount
        self.movement_type = movement_type
        self.statement_details = statement_details
        self.amount_credited_to_merchant_account = amount_credited_to_merchant_account
        self.amount_recieved_at_bank = amount_recieved_at_bank
        self.deposit_country = deposit_country
        self.deposit_date = deposit_date
        self.deposit_reference = deposit_reference
        self.fx_executed_detail = fx_executed_detail
        self.unapplied_reason = unapplied_reason


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
        amount_credited_to_merchant_account = earthport-rest-api-client.models.monetary_value.MonetaryValue.from_dictionary(dictionary.get('amountCreditedToMerchantAccount')) if dictionary.get('amountCreditedToMerchantAccount') else None
        amount_recieved_at_bank = earthport-rest-api-client.models.monetary_value.MonetaryValue.from_dictionary(dictionary.get('amountRecievedAtBank')) if dictionary.get('amountRecievedAtBank') else None
        deposit_country = dictionary.get('depositCountry')
        deposit_date = dictionary.get('depositDate')
        transaction_status = earthport-rest-api-client.models.financial_transaction_status.FinancialTransactionStatus.from_dictionary(dictionary.get('transactionStatus')) if dictionary.get('transactionStatus') else None
        statement_details = None
        if dictionary.get('statementDetails') != None:
            statement_details = list()
            for structure in dictionary.get('statementDetails'):
                statement_details.append(earthport-rest-api-client.models.statement_detail.StatementDetail.from_dictionary(structure))
        deposit_reference = dictionary.get('depositReference')
        fx_executed_detail = earthport-rest-api-client.models.fx_executed_rate.FXExecutedRate.from_dictionary(dictionary.get('fxExecutedDetail')) if dictionary.get('fxExecutedDetail') else None
        unapplied_reason = dictionary.get('unappliedReason')

        # Return an object of this model
        return cls(transaction_id,
                   timestamp,
                   transaction_type,
                   amount,
                   movement_type,
                   amount_credited_to_merchant_account,
                   amount_recieved_at_bank,
                   deposit_country,
                   deposit_date,
                   transaction_status,
                   statement_details,
                   deposit_reference,
                   fx_executed_detail,
                   unapplied_reason)


