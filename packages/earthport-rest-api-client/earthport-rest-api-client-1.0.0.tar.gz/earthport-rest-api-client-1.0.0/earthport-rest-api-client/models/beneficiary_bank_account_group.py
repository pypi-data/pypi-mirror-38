# -*- coding: utf-8 -*-

import earthport-rest-api-client.models.beneficiary_bank_account_fields_list

class BeneficiaryBankAccountGroup(object):

    """Implementation of the 'BeneficiaryBankAccountGroup' model.

    This type defines a bank account data group. Each group is normally
    represented as a row on the UI. 'groupLabel' is the UI test to display as
    a name for this row. 'mandatory' indicates whether values must be supplied
    in the fields of this group.

    Attributes:
        group_label (string): TODO: type description here.
        mandatory (string): TODO: type description here.
        beneficiary_bank_account_fields_list
            (BeneficiaryBankAccountFieldsList): This type defines a bank
            account field.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "group_label":'groupLabel',
        "mandatory":'mandatory',
        "beneficiary_bank_account_fields_list":'beneficiaryBankAccountFieldsList'
    }

    def __init__(self,
                 group_label=None,
                 mandatory=None,
                 beneficiary_bank_account_fields_list=None):
        """Constructor for the BeneficiaryBankAccountGroup class"""

        # Initialize members of the class
        self.group_label = group_label
        self.mandatory = mandatory
        self.beneficiary_bank_account_fields_list = beneficiary_bank_account_fields_list


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
        group_label = dictionary.get('groupLabel')
        mandatory = dictionary.get('mandatory')
        beneficiary_bank_account_fields_list = earthport-rest-api-client.models.beneficiary_bank_account_fields_list.BeneficiaryBankAccountFieldsList.from_dictionary(dictionary.get('beneficiaryBankAccountFieldsList')) if dictionary.get('beneficiaryBankAccountFieldsList') else None

        # Return an object of this model
        return cls(group_label,
                   mandatory,
                   beneficiary_bank_account_fields_list)


