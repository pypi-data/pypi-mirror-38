# -*- coding: utf-8 -*-

import earthport-rest-api-client.models.beneficiary_bank_account_group

class BeneficiaryBankAccountGroupsList(object):

    """Implementation of the 'BeneficiaryBankAccountGroupsList' model.

    This type defines a list of bank account data groups. Each group is
    normally represented as a row on the UI.

    Attributes:
        beneficiary_bank_account_field_group (list of
            BeneficiaryBankAccountGroup): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "beneficiary_bank_account_field_group":'beneficiaryBankAccountFieldGroup'
    }

    def __init__(self,
                 beneficiary_bank_account_field_group=None):
        """Constructor for the BeneficiaryBankAccountGroupsList class"""

        # Initialize members of the class
        self.beneficiary_bank_account_field_group = beneficiary_bank_account_field_group


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
        beneficiary_bank_account_field_group = None
        if dictionary.get('beneficiaryBankAccountFieldGroup') != None:
            beneficiary_bank_account_field_group = list()
            for structure in dictionary.get('beneficiaryBankAccountFieldGroup'):
                beneficiary_bank_account_field_group.append(earthport-rest-api-client.models.beneficiary_bank_account_group.BeneficiaryBankAccountGroup.from_dictionary(structure))

        # Return an object of this model
        return cls(beneficiary_bank_account_field_group)


