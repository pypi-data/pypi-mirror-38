# -*- coding: utf-8 -*-

import earthport-rest-api-client.models.user_id
import earthport-rest-api-client.models.ben_bank_id
import earthport-rest-api-client.models.identity
import earthport-rest-api-client.models.bank_account_details

class GetBeneficiaryBankAccountResponse(object):

    """Implementation of the 'Get Beneficiary Bank AccountResponse' model.

    This type gives a summary of the Beneficiary Bank Account.

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
        is_active (bool): TODO: type description here.
        bank_account_details (list of BankAccountDetails): TODO: type
            description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "user_id":'userID',
        "ben_bank_id":'benBankID',
        "beneficiary_identity":'beneficiaryIdentity',
        "description":'description',
        "country_code":'countryCode',
        "bank_account_details":'bankAccountDetails',
        "currency_code":'currencyCode',
        "is_active":'isActive'
    }

    def __init__(self,
                 user_id=None,
                 ben_bank_id=None,
                 beneficiary_identity=None,
                 description=None,
                 country_code=None,
                 bank_account_details=None,
                 currency_code=None,
                 is_active=None):
        """Constructor for the GetBeneficiaryBankAccountResponse class"""

        # Initialize members of the class
        self.user_id = user_id
        self.ben_bank_id = ben_bank_id
        self.beneficiary_identity = beneficiary_identity
        self.description = description
        self.country_code = country_code
        self.currency_code = currency_code
        self.is_active = is_active
        self.bank_account_details = bank_account_details


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
        user_id = earthport-rest-api-client.models.user_id.UserID.from_dictionary(dictionary.get('userID')) if dictionary.get('userID') else None
        ben_bank_id = earthport-rest-api-client.models.ben_bank_id.BenBankID.from_dictionary(dictionary.get('benBankID')) if dictionary.get('benBankID') else None
        beneficiary_identity = earthport-rest-api-client.models.identity.Identity.from_dictionary(dictionary.get('beneficiaryIdentity')) if dictionary.get('beneficiaryIdentity') else None
        description = dictionary.get('description')
        country_code = dictionary.get('countryCode')
        bank_account_details = None
        if dictionary.get('bankAccountDetails') != None:
            bank_account_details = list()
            for structure in dictionary.get('bankAccountDetails'):
                bank_account_details.append(earthport-rest-api-client.models.bank_account_details.BankAccountDetails.from_dictionary(structure))
        currency_code = dictionary.get('currencyCode')
        is_active = dictionary.get('isActive')

        # Return an object of this model
        return cls(user_id,
                   ben_bank_id,
                   beneficiary_identity,
                   description,
                   country_code,
                   bank_account_details,
                   currency_code,
                   is_active)


