# -*- coding: utf-8 -*-

import earthport-rest-api-client.models.monetary_value
import earthport-rest-api-client.models.users_bank_id

class GetPayoutRequiredDataForBank(object):

    """Implementation of the 'getPayoutRequiredDataForBank' model.

    TODO: type model description here.

    Attributes:
        amount (MonetaryValue): Represents a monetary value containing a
            decimal amount value along with a currency code. The currency code
            is a three letter ISO 4217 code. E.g. GBP for British sterling
            pounds.
        payer (PayerTypeEnum): The Payer Type is optional. If no Payer Type is
            specified then the default value of authenticatedCaller will be
            used.
        service_level (ServiceLevelEnum): Supported service levels for a
            payout request (standard or express).
        users_bank_id (UsersBankID): This group consists of a collection of
            both the user ID group and beneficiary bank ID group. The 'userID'
            is a collection of user identifier types. The 'benBankID' is a
            collection of account identifier types. Both the 'userID' and
            'benBankID' fields are mandatory.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "users_bank_id":'usersBankID',
        "amount":'amount',
        "payer":'payer',
        "service_level":'serviceLevel'
    }

    def __init__(self,
                 users_bank_id=None,
                 amount=None,
                 payer=None,
                 service_level=None):
        """Constructor for the GetPayoutRequiredDataForBank class"""

        # Initialize members of the class
        self.amount = amount
        self.payer = payer
        self.service_level = service_level
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
        users_bank_id = earthport-rest-api-client.models.users_bank_id.UsersBankID.from_dictionary(dictionary.get('usersBankID')) if dictionary.get('usersBankID') else None
        amount = earthport-rest-api-client.models.monetary_value.MonetaryValue.from_dictionary(dictionary.get('amount')) if dictionary.get('amount') else None
        payer = dictionary.get('payer')
        service_level = dictionary.get('serviceLevel')

        # Return an object of this model
        return cls(users_bank_id,
                   amount,
                   payer,
                   service_level)


