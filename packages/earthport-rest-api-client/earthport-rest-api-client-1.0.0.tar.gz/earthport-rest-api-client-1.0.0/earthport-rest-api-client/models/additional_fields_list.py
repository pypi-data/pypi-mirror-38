# -*- coding: utf-8 -*-

import earthport-rest-api-client.models.additional_field_with_validator
import earthport-rest-api-client.models.additional_field_with_values

class AdditionalFieldsList(object):

    """Implementation of the 'additionalFieldsList' model.

    Additional fields will be one of two types; free text or list options.
    'additionalFieldWithValues' gives a list of acceptable responses.
    'additionalFieldWithValidator' is a free text response.

    Attributes:
        additional_field_with_validator (list of
            AdditionalFieldWithValidator): TODO: type description here.
        additional_field_with_values (list of AdditionalFieldWithValues):
            TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "additional_field_with_validator":'additionalFieldWithValidator',
        "additional_field_with_values":'additionalFieldWithValues'
    }

    def __init__(self,
                 additional_field_with_validator=None,
                 additional_field_with_values=None):
        """Constructor for the AdditionalFieldsList class"""

        # Initialize members of the class
        self.additional_field_with_validator = additional_field_with_validator
        self.additional_field_with_values = additional_field_with_values


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
        additional_field_with_validator = None
        if dictionary.get('additionalFieldWithValidator') != None:
            additional_field_with_validator = list()
            for structure in dictionary.get('additionalFieldWithValidator'):
                additional_field_with_validator.append(earthport-rest-api-client.models.additional_field_with_validator.AdditionalFieldWithValidator.from_dictionary(structure))
        additional_field_with_values = None
        if dictionary.get('additionalFieldWithValues') != None:
            additional_field_with_values = list()
            for structure in dictionary.get('additionalFieldWithValues'):
                additional_field_with_values.append(earthport-rest-api-client.models.additional_field_with_values.AdditionalFieldWithValues.from_dictionary(structure))

        # Return an object of this model
        return cls(additional_field_with_validator,
                   additional_field_with_values)


