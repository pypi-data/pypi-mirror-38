# -*- coding: utf-8 -*-


class FieldValue(object):

    """Implementation of the 'FieldValue' model.

    TODO: type model description here.

    Attributes:
        label (string): TODO: type description here.
        option (string): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "label":'label',
        "option":'option'
    }

    def __init__(self,
                 label=None,
                 option=None):
        """Constructor for the FieldValue class"""

        # Initialize members of the class
        self.label = label
        self.option = option


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
        label = dictionary.get('label')
        option = dictionary.get('option')

        # Return an object of this model
        return cls(label,
                   option)


