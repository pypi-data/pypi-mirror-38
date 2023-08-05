# -*- coding: utf-8 -*-

import earthport-rest-api-client.models.beneficiary_identity_group
import earthport-rest-api-client.models.beneficiary_identity_field_group_choice

class BeneficiaryIdentityGroupsList(object):

    """Implementation of the 'BeneficiaryIdentityGroupsList' model.

    This type defines a list of identity data groups. Each group is normally
    represented as a section of fields on the UI.

    Attributes:
        group_label (string): TODO: type description here.
        beneficiary_identity_field_group (list of BeneficiaryIdentityGroup):
            TODO: type description here.
        beneficiary_identity_field_group_choice (list of
            BeneficiaryIdentityFieldGroupChoice): TODO: type description
            here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "group_label":'groupLabel',
        "beneficiary_identity_field_group":'beneficiaryIdentityFieldGroup',
        "beneficiary_identity_field_group_choice":'beneficiaryIdentityFieldGroupChoice'
    }

    def __init__(self,
                 group_label=None,
                 beneficiary_identity_field_group=None,
                 beneficiary_identity_field_group_choice=None):
        """Constructor for the BeneficiaryIdentityGroupsList class"""

        # Initialize members of the class
        self.group_label = group_label
        self.beneficiary_identity_field_group = beneficiary_identity_field_group
        self.beneficiary_identity_field_group_choice = beneficiary_identity_field_group_choice


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
        beneficiary_identity_field_group = None
        if dictionary.get('beneficiaryIdentityFieldGroup') != None:
            beneficiary_identity_field_group = list()
            for structure in dictionary.get('beneficiaryIdentityFieldGroup'):
                beneficiary_identity_field_group.append(earthport-rest-api-client.models.beneficiary_identity_group.BeneficiaryIdentityGroup.from_dictionary(structure))
        beneficiary_identity_field_group_choice = None
        if dictionary.get('beneficiaryIdentityFieldGroupChoice') != None:
            beneficiary_identity_field_group_choice = list()
            for structure in dictionary.get('beneficiaryIdentityFieldGroupChoice'):
                beneficiary_identity_field_group_choice.append(earthport-rest-api-client.models.beneficiary_identity_field_group_choice.BeneficiaryIdentityFieldGroupChoice.from_dictionary(structure))

        # Return an object of this model
        return cls(group_label,
                   beneficiary_identity_field_group,
                   beneficiary_identity_field_group_choice)


