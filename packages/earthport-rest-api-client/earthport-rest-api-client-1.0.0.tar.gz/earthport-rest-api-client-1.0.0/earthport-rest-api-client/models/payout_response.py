# -*- coding: utf-8 -*-

import earthport-rest-api-client.models.user_id
import earthport-rest-api-client.models.ben_bank_id
import earthport-rest-api-client.models.transaction_id
import earthport-rest-api-client.models.monetary_value
import earthport-rest-api-client.models.fx_rate

class PayoutResponse(object):

    """Implementation of the 'PayoutResponse' model.

    Response object to the payout request APIs.

    Attributes:
        user_id (UserID): This group consists of all possible user identifier
            types. The 'epUserID' field is a unique identifier for a merchant
            and is the equivalent of a Virtual Account Number (VAN). The
            'merchantUserID' is a merchant specified identifier for an
            individual or company that an account was set up for. The
            'epUserID', 'merchantUserID' or both 'epUserID' and
            'merchantUserID' can be supplied. A mapping will be performed to
            retrieve the merchant user ID from the supplied EP user ID and
            vice versa. If both the 'epUserID' and 'merchantUserID' are
            supplied, a check will be performed to ensure that the two are
            mapped. If the two provided fields are not mapped, then a
            validation error code will be returned. At least one of the fields
            must be populated.
        ben_bank_id (BenBankID): This group consists of all possible
            beneficiary bank identifier types. The 'epBankID' field is a
            unique identifier for a beneficiary bank account. The
            'merchantBankID' is an optional merchant specified identifier for
            the beneficiary bank account. The 'epBankID', 'merchantBankID' or
            both 'epBankID' and 'merchantBankID' can be supplied. A mapping
            will be performed to retrieve the merchant bank ID from the
            supplied EP bank ID and vice versa. If both the 'epBankID' and
            'merchantBankID' are supplied, a check will be performed to ensure
            that the two are mapped. If the two provided fields are not
            mapped, then a validation error code will be returned. At least
            one of the fields must be populated.
        transaction_id (TransactionID): Transaction ID type which contains
            both the unique Earthport transaction ID and the merchant supplied
            transaction ID.
        correspondent_charges_expected (bool): A flag to indicate if
            correspondent charges are expected during the processing of the
            payout request.
        liquidity_value (MonetaryValue): Represents a monetary value
            containing a decimal amount value along with a currency code. The
            currency code is a three letter ISO 4217 code. E.g. GBP for
            British sterling pounds.
        settlement_value (MonetaryValue): Represents a monetary value
            containing a decimal amount value along with a currency code. The
            currency code is a three letter ISO 4217 code. E.g. GBP for
            British sterling pounds.
        fee_value (MonetaryValue): Represents a monetary value containing a
            decimal amount value along with a currency code. The currency code
            is a three letter ISO 4217 code. E.g. GBP for British sterling
            pounds.
        fx_method_expected (FXMethodEnum): Method of FX that will be used to
            settle the payout request.
        fx_rate (FXRate): Represents an FX rate between two currencies, the
            rate is restricted to 6 decimal places. The currency code is a
            three letter ISO 4217 code. E.g. GBP for British sterling pounds.
        accepted_date (string): TODO: type description here.
        expected_settlement_date (string): Valid ISO 8601 date format
            YYYY-MM-DD.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "transaction_id":'transactionID',
        "liquidity_value":'liquidityValue',
        "settlement_value":'settlementValue',
        "user_id":'userID',
        "ben_bank_id":'benBankID',
        "correspondent_charges_expected":'correspondentChargesExpected',
        "fee_value":'feeValue',
        "fx_method_expected":'fxMethodExpected',
        "fx_rate":'fxRate',
        "accepted_date":'acceptedDate',
        "expected_settlement_date":'expectedSettlementDate'
    }

    def __init__(self,
                 transaction_id=None,
                 liquidity_value=None,
                 settlement_value=None,
                 user_id=None,
                 ben_bank_id=None,
                 correspondent_charges_expected=None,
                 fee_value=None,
                 fx_method_expected=None,
                 fx_rate=None,
                 accepted_date=None,
                 expected_settlement_date=None):
        """Constructor for the PayoutResponse class"""

        # Initialize members of the class
        self.user_id = user_id
        self.ben_bank_id = ben_bank_id
        self.transaction_id = transaction_id
        self.correspondent_charges_expected = correspondent_charges_expected
        self.liquidity_value = liquidity_value
        self.settlement_value = settlement_value
        self.fee_value = fee_value
        self.fx_method_expected = fx_method_expected
        self.fx_rate = fx_rate
        self.accepted_date = accepted_date
        self.expected_settlement_date = expected_settlement_date


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
        liquidity_value = earthport-rest-api-client.models.monetary_value.MonetaryValue.from_dictionary(dictionary.get('liquidityValue')) if dictionary.get('liquidityValue') else None
        settlement_value = earthport-rest-api-client.models.monetary_value.MonetaryValue.from_dictionary(dictionary.get('settlementValue')) if dictionary.get('settlementValue') else None
        user_id = earthport-rest-api-client.models.user_id.UserID.from_dictionary(dictionary.get('userID')) if dictionary.get('userID') else None
        ben_bank_id = earthport-rest-api-client.models.ben_bank_id.BenBankID.from_dictionary(dictionary.get('benBankID')) if dictionary.get('benBankID') else None
        correspondent_charges_expected = dictionary.get('correspondentChargesExpected')
        fee_value = earthport-rest-api-client.models.monetary_value.MonetaryValue.from_dictionary(dictionary.get('feeValue')) if dictionary.get('feeValue') else None
        fx_method_expected = dictionary.get('fxMethodExpected')
        fx_rate = earthport-rest-api-client.models.fx_rate.FXRate.from_dictionary(dictionary.get('fxRate')) if dictionary.get('fxRate') else None
        accepted_date = dictionary.get('acceptedDate')
        expected_settlement_date = dictionary.get('expectedSettlementDate')

        # Return an object of this model
        return cls(transaction_id,
                   liquidity_value,
                   settlement_value,
                   user_id,
                   ben_bank_id,
                   correspondent_charges_expected,
                   fee_value,
                   fx_method_expected,
                   fx_rate,
                   accepted_date,
                   expected_settlement_date)


