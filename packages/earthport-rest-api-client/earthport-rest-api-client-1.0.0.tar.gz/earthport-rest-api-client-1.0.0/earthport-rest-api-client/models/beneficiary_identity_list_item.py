# -*- coding: utf-8 -*-


class BeneficiaryIdentityListItem(object):

    """Implementation of the 'BeneficiaryIdentityListItem' model.

    TODO: type model description here.

    Attributes:
        label (string): TODO: type description here.
        value (string): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "label":'label',
        "value":'value'
    }

    def __init__(self,
                 label=None,
                 value=None):
        """Constructor for the BeneficiaryIdentityListItem class"""

        # Initialize members of the class
        self.label = label
        self.value = value


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
        value = dictionary.get('value')

        # Return an object of this model
        return cls(label,
                   value)


