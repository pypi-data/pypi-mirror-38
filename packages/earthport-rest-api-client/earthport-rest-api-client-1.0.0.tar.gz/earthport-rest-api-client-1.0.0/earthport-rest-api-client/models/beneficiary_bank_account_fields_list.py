# -*- coding: utf-8 -*-

import earthport-rest-api-client.models.beneficiary_bank_account_field

class BeneficiaryBankAccountFieldsList(object):

    """Implementation of the 'BeneficiaryBankAccountFieldsList' model.

    This type defines a bank account field.

    Attributes:
        beneficiary_bank_account_field (list of BeneficiaryBankAccountField):
            TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "beneficiary_bank_account_field":'beneficiaryBankAccountField'
    }

    def __init__(self,
                 beneficiary_bank_account_field=None):
        """Constructor for the BeneficiaryBankAccountFieldsList class"""

        # Initialize members of the class
        self.beneficiary_bank_account_field = beneficiary_bank_account_field


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
        beneficiary_bank_account_field = None
        if dictionary.get('beneficiaryBankAccountField') != None:
            beneficiary_bank_account_field = list()
            for structure in dictionary.get('beneficiaryBankAccountField'):
                beneficiary_bank_account_field.append(earthport-rest-api-client.models.beneficiary_bank_account_field.BeneficiaryBankAccountField.from_dictionary(structure))

        # Return an object of this model
        return cls(beneficiary_bank_account_field)


