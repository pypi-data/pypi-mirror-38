# -*- coding: utf-8 -*-

import earthport-rest-api-client.models.ben_bank_id
import earthport-rest-api-client.models.bank_account_details

class BeneficiaryBankAccountSummary(object):

    """Implementation of the 'BeneficiaryBankAccountSummary' model.

    TODO: type model description here.

    Attributes:
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
        description (string): Type which defines a beneficiary bank account
            description. Each bank account must be given a description
            therefore this is a mandatory component of the
            BeneficiaryBankAccount complex type.
        country_code (string): Valid supported ISO 3166 2-character country
            code.
        bank_account_details (list of BankAccountDetails): TODO: type
            description here.
        status (string): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "ben_bank_id":'benBankID',
        "description":'description',
        "country_code":'countryCode',
        "bank_account_details":'bankAccountDetails',
        "status":'status'
    }

    def __init__(self,
                 ben_bank_id=None,
                 description=None,
                 country_code=None,
                 bank_account_details=None,
                 status=None):
        """Constructor for the BeneficiaryBankAccountSummary class"""

        # Initialize members of the class
        self.ben_bank_id = ben_bank_id
        self.description = description
        self.country_code = country_code
        self.bank_account_details = bank_account_details
        self.status = status


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
        ben_bank_id = earthport-rest-api-client.models.ben_bank_id.BenBankID.from_dictionary(dictionary.get('benBankID')) if dictionary.get('benBankID') else None
        description = dictionary.get('description')
        country_code = dictionary.get('countryCode')
        bank_account_details = None
        if dictionary.get('bankAccountDetails') != None:
            bank_account_details = list()
            for structure in dictionary.get('bankAccountDetails'):
                bank_account_details.append(earthport-rest-api-client.models.bank_account_details.BankAccountDetails.from_dictionary(structure))
        status = dictionary.get('status')

        # Return an object of this model
        return cls(ben_bank_id,
                   description,
                   country_code,
                   bank_account_details,
                   status)


