# -*- coding: utf-8 -*-

import earthport-rest-api-client.models.ben_bank_id_merchant
import earthport-rest-api-client.models.identity
import earthport-rest-api-client.models.bank_account_details

class CreateBeneficiaryBankAccountRequest(object):

    """Implementation of the 'CreateBeneficiaryBankAccountRequest' model.

    The beneficiary bank account Object.

    Attributes:
        ben_bank_id (BenBankIDMerchant): This group consists of merchant
            beneficiary bank identifier only.
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
        bank_account_details (list of BankAccountDetails): TODO: type
            description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "beneficiary_identity":'beneficiaryIdentity',
        "description":'description',
        "country_code":'countryCode',
        "bank_account_details":'bankAccountDetails',
        "ben_bank_id":'benBankID',
        "currency_code":'currencyCode'
    }

    def __init__(self,
                 beneficiary_identity=None,
                 description=None,
                 country_code=None,
                 bank_account_details=None,
                 ben_bank_id=None,
                 currency_code=None):
        """Constructor for the CreateBeneficiaryBankAccountRequest class"""

        # Initialize members of the class
        self.ben_bank_id = ben_bank_id
        self.beneficiary_identity = beneficiary_identity
        self.description = description
        self.country_code = country_code
        self.currency_code = currency_code
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
        beneficiary_identity = earthport-rest-api-client.models.identity.Identity.from_dictionary(dictionary.get('beneficiaryIdentity')) if dictionary.get('beneficiaryIdentity') else None
        description = dictionary.get('description')
        country_code = dictionary.get('countryCode')
        bank_account_details = None
        if dictionary.get('bankAccountDetails') != None:
            bank_account_details = list()
            for structure in dictionary.get('bankAccountDetails'):
                bank_account_details.append(earthport-rest-api-client.models.bank_account_details.BankAccountDetails.from_dictionary(structure))
        ben_bank_id = earthport-rest-api-client.models.ben_bank_id_merchant.BenBankIDMerchant.from_dictionary(dictionary.get('benBankID')) if dictionary.get('benBankID') else None
        currency_code = dictionary.get('currencyCode')

        # Return an object of this model
        return cls(beneficiary_identity,
                   description,
                   country_code,
                   bank_account_details,
                   ben_bank_id,
                   currency_code)


