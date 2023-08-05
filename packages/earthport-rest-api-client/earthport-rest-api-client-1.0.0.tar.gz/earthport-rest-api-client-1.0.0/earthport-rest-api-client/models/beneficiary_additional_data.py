# -*- coding: utf-8 -*-


class BeneficiaryAdditionalData(object):

    """Implementation of the 'BeneficiaryAdditionalData' model.

    Represents a set of name value pairs that can be supplied with the
    Identity information. The keys will be validated on the server side
    against a list of valid types that are accepted. Both the key and the
    value are required if adding additional data The length of the
    additionalDataKey field is currently restricted to 50 bytes. The length of
    the additionalDataValue field is currently restricted to 1024.

    Attributes:
        additional_data_key (string): TODO: type description here.
        additional_data_value (string): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "additional_data_key":'additionalDataKey',
        "additional_data_value":'additionalDataValue'
    }

    def __init__(self,
                 additional_data_key=None,
                 additional_data_value=None):
        """Constructor for the BeneficiaryAdditionalData class"""

        # Initialize members of the class
        self.additional_data_key = additional_data_key
        self.additional_data_value = additional_data_value


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
        additional_data_key = dictionary.get('additionalDataKey')
        additional_data_value = dictionary.get('additionalDataValue')

        # Return an object of this model
        return cls(additional_data_key,
                   additional_data_value)


