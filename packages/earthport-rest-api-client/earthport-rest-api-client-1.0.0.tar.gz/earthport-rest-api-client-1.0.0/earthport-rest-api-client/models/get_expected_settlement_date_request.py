# -*- coding: utf-8 -*-

import earthport-rest-api-client.models.identity
import earthport-rest-api-client.models.bank_account_details
import earthport-rest-api-client.models.payout_details
import earthport-rest-api-client.models.transaction_hold

class GetExpectedSettlementDateRequest(object):

    """Implementation of the 'GetExpectedSettlementDateRequest' model.

    The beneficiary bank account Object.

    Attributes:
        beneficiary_identity (Identity): Represents the identity of an
            individual or legal entity. You must specify one of either an
            individual identity or legal entity identity or unstructured
            identity.
        description (string): Type which defines a beneficiary bank account
            description. Each bank account must be given a description
            therefore this is a mandatory component of the
            BeneficiaryBankAccount complex type.
        country_code (string): Valid supported ISO 3166 2-character country
            code.
        currency_code (string): Valid supported ISO 4217 3-character currency
            code.
        payout_request_currency (string): Valid supported ISO 4217 3-character
            currency code.
        anticipated_payout_request_time (string): Valid ISO 8601 date format
            YYYY-MM-DD.
        bank_account_details (list of BankAccountDetails): TODO: type
            description here.
        payer_identity (Identity): Represents the identity of an individual or
            legal entity. You must specify one of either an individual
            identity or legal entity identity or unstructured identity.
        service_level (ServiceLevelEnum): Supported service levels for a
            payout request (standard or express).
        payer_type (PayerTypeEnum): The type of Payer making the payment. This
            detrmines which identity details are used as the payer identity.
        payout_details (list of PayoutDetails): TODO: type description here.
        transaction_hold (TransactionHold): Parameter to prevent transactions
            from being processed until the desired time has been reached Note
            releaseDateTime must be in UTC format.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "beneficiary_identity":'beneficiaryIdentity',
        "description":'description',
        "country_code":'countryCode',
        "anticipated_payout_request_time":'anticipatedPayoutRequestTime',
        "bank_account_details":'bankAccountDetails',
        "payout_details":'payoutDetails',
        "currency_code":'currencyCode',
        "payout_request_currency":'payoutRequestCurrency',
        "payer_identity":'payerIdentity',
        "service_level":'serviceLevel',
        "payer_type":'payerType',
        "transaction_hold":'transactionHold'
    }

    def __init__(self,
                 beneficiary_identity=None,
                 description=None,
                 country_code=None,
                 anticipated_payout_request_time=None,
                 bank_account_details=None,
                 payout_details=None,
                 currency_code=None,
                 payout_request_currency=None,
                 payer_identity=None,
                 service_level=None,
                 payer_type=None,
                 transaction_hold=None):
        """Constructor for the GetExpectedSettlementDateRequest class"""

        # Initialize members of the class
        self.beneficiary_identity = beneficiary_identity
        self.description = description
        self.country_code = country_code
        self.currency_code = currency_code
        self.payout_request_currency = payout_request_currency
        self.anticipated_payout_request_time = anticipated_payout_request_time
        self.bank_account_details = bank_account_details
        self.payer_identity = payer_identity
        self.service_level = service_level
        self.payer_type = payer_type
        self.payout_details = payout_details
        self.transaction_hold = transaction_hold


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
        beneficiary_identity = earthport-rest-api-client.models.identity.Identity.from_dictionary(dictionary.get('beneficiaryIdentity')) if dictionary.get('beneficiaryIdentity') else None
        description = dictionary.get('description')
        country_code = dictionary.get('countryCode')
        anticipated_payout_request_time = dictionary.get('anticipatedPayoutRequestTime')
        bank_account_details = None
        if dictionary.get('bankAccountDetails') != None:
            bank_account_details = list()
            for structure in dictionary.get('bankAccountDetails'):
                bank_account_details.append(earthport-rest-api-client.models.bank_account_details.BankAccountDetails.from_dictionary(structure))
        payout_details = None
        if dictionary.get('payoutDetails') != None:
            payout_details = list()
            for structure in dictionary.get('payoutDetails'):
                payout_details.append(earthport-rest-api-client.models.payout_details.PayoutDetails.from_dictionary(structure))
        currency_code = dictionary.get('currencyCode')
        payout_request_currency = dictionary.get('payoutRequestCurrency')
        payer_identity = earthport-rest-api-client.models.identity.Identity.from_dictionary(dictionary.get('payerIdentity')) if dictionary.get('payerIdentity') else None
        service_level = dictionary.get('serviceLevel')
        payer_type = dictionary.get('payerType')
        transaction_hold = earthport-rest-api-client.models.transaction_hold.TransactionHold.from_dictionary(dictionary.get('transactionHold')) if dictionary.get('transactionHold') else None

        # Return an object of this model
        return cls(beneficiary_identity,
                   description,
                   country_code,
                   anticipated_payout_request_time,
                   bank_account_details,
                   payout_details,
                   currency_code,
                   payout_request_currency,
                   payer_identity,
                   service_level,
                   payer_type,
                   transaction_hold)


