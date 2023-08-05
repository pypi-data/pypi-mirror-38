# -*- coding: utf-8 -*-

import earthport-rest-api-client.models.beneficiary_identity_list_item

class BeneficiaryIdentityListItems(object):

    """Implementation of the 'BeneficiaryIdentityListItems' model.

    The beneficiaryIdentityField contains optional listItem sub-elements. The
    listItem sub-elements would normally be present where the inputType
    attribute is 'list'.

    Attributes:
        beneficiary_identity_field (list of BeneficiaryIdentityListItem):
            TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "beneficiary_identity_field":'beneficiaryIdentityField'
    }

    def __init__(self,
                 beneficiary_identity_field=None):
        """Constructor for the BeneficiaryIdentityListItems class"""

        # Initialize members of the class
        self.beneficiary_identity_field = beneficiary_identity_field


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
        beneficiary_identity_field = None
        if dictionary.get('beneficiaryIdentityField') != None:
            beneficiary_identity_field = list()
            for structure in dictionary.get('beneficiaryIdentityField'):
                beneficiary_identity_field.append(earthport-rest-api-client.models.beneficiary_identity_list_item.BeneficiaryIdentityListItem.from_dictionary(structure))

        # Return an object of this model
        return cls(beneficiary_identity_field)


