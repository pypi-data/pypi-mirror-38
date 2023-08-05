# -*- coding: utf-8 -*-

import earthport-rest-api-client.models.user_id_merchant
import earthport-rest-api-client.models.identity

class User(object):

    """Implementation of the 'User' model.

    A user Object.

    Attributes:
        user_id (UserIDMerchant): This group consists of merchant user
            identifier only.
        managed_merchant_identity (string): Refers to the descriptive name
            used to identify a given merchant. It is unique across Earthport
            merchants.
        account_currency (string): Valid supported ISO 4217 3-character
            currency code.
        payer_identity (Identity): Represents the identity of an individual or
            legal entity. You must specify one of either an individual
            identity or legal entity identity or unstructured identity.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "payer_identity":'payerIdentity',
        "user_id":'userID',
        "managed_merchant_identity":'managedMerchantIdentity',
        "account_currency":'accountCurrency'
    }

    def __init__(self,
                 payer_identity=None,
                 user_id=None,
                 managed_merchant_identity=None,
                 account_currency=None):
        """Constructor for the User class"""

        # Initialize members of the class
        self.user_id = user_id
        self.managed_merchant_identity = managed_merchant_identity
        self.account_currency = account_currency
        self.payer_identity = payer_identity


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
        payer_identity = earthport-rest-api-client.models.identity.Identity.from_dictionary(dictionary.get('payerIdentity')) if dictionary.get('payerIdentity') else None
        user_id = earthport-rest-api-client.models.user_id_merchant.UserIDMerchant.from_dictionary(dictionary.get('userID')) if dictionary.get('userID') else None
        managed_merchant_identity = dictionary.get('managedMerchantIdentity')
        account_currency = dictionary.get('accountCurrency')

        # Return an object of this model
        return cls(payer_identity,
                   user_id,
                   managed_merchant_identity,
                   account_currency)


