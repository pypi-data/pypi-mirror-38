# -*- coding: utf-8 -*-

import earthport-rest-api-client.models.additional_fields_list
import earthport-rest-api-client.models.identity_restriction

class PurposeOfPaymentUsageRestrictions(object):

    """Implementation of the 'purposeOfPaymentUsageRestrictions' model.

    Usage restrictions apply where a specified code is only acceptable for a
    given type of payer or beneficiary. This attribute indicates whether the
    code can be used for Individuals and/or Legal Entities, for both payer and
    beneficiary parties. Additional field specifications identify further data
    that is required, given the chosen Purpose of Payment.

    Attributes:
        additional_fields_list (AdditionalFieldsList): Additional fields will
            be one of two types; free text or list options.
            'additionalFieldWithValues' gives a list of acceptable responses.
            'additionalFieldWithValidator' is a free text response.
        beneficiary (IdentityRestriction): TODO: type description here.
        originator (IdentityRestriction): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "additional_fields_list":'additionalFieldsList',
        "beneficiary":'beneficiary',
        "originator":'originator'
    }

    def __init__(self,
                 additional_fields_list=None,
                 beneficiary=None,
                 originator=None):
        """Constructor for the PurposeOfPaymentUsageRestrictions class"""

        # Initialize members of the class
        self.additional_fields_list = additional_fields_list
        self.beneficiary = beneficiary
        self.originator = originator


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
        additional_fields_list = earthport-rest-api-client.models.additional_fields_list.AdditionalFieldsList.from_dictionary(dictionary.get('additionalFieldsList')) if dictionary.get('additionalFieldsList') else None
        beneficiary = earthport-rest-api-client.models.identity_restriction.IdentityRestriction.from_dictionary(dictionary.get('beneficiary')) if dictionary.get('beneficiary') else None
        originator = earthport-rest-api-client.models.identity_restriction.IdentityRestriction.from_dictionary(dictionary.get('originator')) if dictionary.get('originator') else None

        # Return an object of this model
        return cls(additional_fields_list,
                   beneficiary,
                   originator)


