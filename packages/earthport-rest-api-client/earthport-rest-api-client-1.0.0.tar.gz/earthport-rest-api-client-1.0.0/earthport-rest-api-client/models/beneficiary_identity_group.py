# -*- coding: utf-8 -*-

import earthport-rest-api-client.models.beneficiary_identity_fields_list

class BeneficiaryIdentityGroup(object):

    """Implementation of the 'BeneficiaryIdentityGroup' model.

    This type defines a beneficiary identity data group. Each group is
    normally represented as a section of fields on the UI. 'groupLabel' is the
    UI test to display as a name for this section. 'mandatory' indicates
    whether all section is mandatory. 'elementName' is the name of the element
    in the addBeneficiaryBankAccount request document for the corresponding
    section.

    Attributes:
        element_name (string): TODO: type description here.
        group_label (string): TODO: type description here.
        mandatory (string): TODO: type description here.
        beneficiary_identity_fields_list (BeneficiaryIdentityFieldsList): This
            type defines a identity fields list.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "element_name":'elementName',
        "group_label":'groupLabel',
        "mandatory":'mandatory',
        "beneficiary_identity_fields_list":'beneficiaryIdentityFieldsList'
    }

    def __init__(self,
                 element_name=None,
                 group_label=None,
                 mandatory=None,
                 beneficiary_identity_fields_list=None):
        """Constructor for the BeneficiaryIdentityGroup class"""

        # Initialize members of the class
        self.element_name = element_name
        self.group_label = group_label
        self.mandatory = mandatory
        self.beneficiary_identity_fields_list = beneficiary_identity_fields_list


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
        element_name = dictionary.get('elementName')
        group_label = dictionary.get('groupLabel')
        mandatory = dictionary.get('mandatory')
        beneficiary_identity_fields_list = earthport-rest-api-client.models.beneficiary_identity_fields_list.BeneficiaryIdentityFieldsList.from_dictionary(dictionary.get('beneficiaryIdentityFieldsList')) if dictionary.get('beneficiaryIdentityFieldsList') else None

        # Return an object of this model
        return cls(element_name,
                   group_label,
                   mandatory,
                   beneficiary_identity_fields_list)


