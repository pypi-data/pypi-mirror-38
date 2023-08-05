# -*- coding: utf-8 -*-

import earthport-rest-api-client.models.beneficiary_identity_field

class BeneficiaryIdentityFieldsList(object):

    """Implementation of the 'BeneficiaryIdentityFieldsList' model.

    This type defines a identity fields list.

    Attributes:
        beneficiary_identity_field (list of BeneficiaryIdentityField): TODO:
            type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "beneficiary_identity_field":'beneficiaryIdentityField'
    }

    def __init__(self,
                 beneficiary_identity_field=None):
        """Constructor for the BeneficiaryIdentityFieldsList class"""

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
                beneficiary_identity_field.append(earthport-rest-api-client.models.beneficiary_identity_field.BeneficiaryIdentityField.from_dictionary(structure))

        # Return an object of this model
        return cls(beneficiary_identity_field)


