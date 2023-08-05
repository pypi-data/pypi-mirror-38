# -*- coding: utf-8 -*-

import earthport-rest-api-client.models.beneficiary_identity_groups_list

class BeneficiaryIdentityFieldGroupChoice(object):

    """Implementation of the 'BeneficiaryIdentityFieldGroupChoice' model.

    This type defines that in common case at least one of the nested groups
    should be included into addBeneficiaryBankAccount request document. On UI
    it can be presented with drop-down list containing nested groups labels.
    'minElementNum' minimum this number of the nested groups should be
    specified (1 by default). 'maxElementNum' maximum this number of the
    nested groups can be specified (1 by default).

    Attributes:
        max_groups_list_num (int): TODO: type description here.
        min_groups_list_num (int): TODO: type description here.
        beneficiary_identity_field_groups_list (list of
            BeneficiaryIdentityGroupsList): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "max_groups_list_num":'maxGroupsListNum',
        "min_groups_list_num":'minGroupsListNum',
        "beneficiary_identity_field_groups_list":'beneficiaryIdentityFieldGroupsList'
    }

    def __init__(self,
                 max_groups_list_num=None,
                 min_groups_list_num=None,
                 beneficiary_identity_field_groups_list=None):
        """Constructor for the BeneficiaryIdentityFieldGroupChoice class"""

        # Initialize members of the class
        self.max_groups_list_num = max_groups_list_num
        self.min_groups_list_num = min_groups_list_num
        self.beneficiary_identity_field_groups_list = beneficiary_identity_field_groups_list


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
        max_groups_list_num = dictionary.get('maxGroupsListNum')
        min_groups_list_num = dictionary.get('minGroupsListNum')
        beneficiary_identity_field_groups_list = None
        if dictionary.get('beneficiaryIdentityFieldGroupsList') != None:
            beneficiary_identity_field_groups_list = list()
            for structure in dictionary.get('beneficiaryIdentityFieldGroupsList'):
                beneficiary_identity_field_groups_list.append(earthport-rest-api-client.models.beneficiary_identity_groups_list.BeneficiaryIdentityGroupsList.from_dictionary(structure))

        # Return an object of this model
        return cls(max_groups_list_num,
                   min_groups_list_num,
                   beneficiary_identity_field_groups_list)


